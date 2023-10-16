import hashlib
import os
import tempfile
import zipfile
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Union

import numpy as np
import pydicom
import pydicom.errors
import pydicom.multival
import pydicom.tag
import SimpleITK as sitk

from dicomselect.dicom import DEFAULT_DICOM_TAGS, DICOMTag, InvalidTagError

PathLike = os.PathLike


class UnreadableDICOMError(BaseException):
    """Exception raised when a DICOM series could not be loaded"""

    def __init__(self, path: PathLike):
        super().__init__(f'Could not read {path} using either SimpleITK or pydicom')


class MissingDICOMFilesError(BaseException):
    """Exception raised when a DICOM series has missing DICOM slices"""

    def __init__(self, path: PathLike):
        super().__init__(f"Missing DICOM slices detected in {path}")


def get_orientation(
        image_direction: Iterable[float],
):
    """
    Deduce image orientation from DICOM Image Orientation (Patient) Attribute.
    Based on https://gist.github.com/agirault/60a72bdaea4a2126ecd08912137fe641
    and https://stackoverflow.com/questions/70645577/translate-image-orientation-into-axial-sagittal-or-coronal-plane
    and https://stackoverflow.com/questions/69799946/simpleitk-getdirection-explained
    """
    if len(image_direction) != 9:
        return "unknown"

    Ax, Bx, Cx, Ay, By, Cy, Az, Bz, Cz = image_direction
    C = (Cx, Cy, Cz)

    abs_image_z = np.abs(C)
    main_index = list(abs_image_z).index(max(abs_image_z))
    if main_index == 0:
        main_direction = "sagittal"
    elif main_index == 1:
        main_direction = "coronal"
    else:
        main_direction = "transverse"
    return main_direction


def get_pydicom_value(ds: pydicom.dataset.Dataset, key: Union[pydicom.tag.BaseTag, str]) -> str:
    if isinstance(key, str):
        key = '0x' + key.replace('|', '')
    if key in ds:
        result = ds[key]
        if result.is_empty:
            return ''
        result = result.value
        if isinstance(result, (list, pydicom.multival.MultiValue)):
            result = "\\".join([str(v) for v in result])
        return str(result)
    return ''


def get_orientation_matrix(ds: pydicom.FileDataset) -> np.ndarray:
    x, y = np.array(list(map(float, ds.ImageOrientationPatient))).reshape(2, 3)
    return np.stack([x, y, np.cross(x, y)])


def filter_localizer_slices(dicom_slice_paths: List[str]) -> List[str]:
    """
    Filter out localizer slices (slices with ImageType == LOCALIZER).
    WARNING: this is slow and a heuristic that may not work for all datasets.
    """
    filtered_dicom_slice_paths = []
    for path in dicom_slice_paths:
        reader = sitk.ImageFileReader()
        reader.SetFileName(str(path))
        reader.LoadPrivateTagsOn()
        reader.ReadImageInformation()
        image_type = reader.GetMetaData("0008|0008")
        if "LOCALIZER" not in image_type.upper():
            filtered_dicom_slice_paths.append(path)
    return filtered_dicom_slice_paths


class DICOMImageReader:
    """
    Read folder containing DICOM slices (possibly enclosed in a 'dicom.zip' file).
    If both DICOM slices and a 'dicom.zip' file are present, the dicom.zip used.

    Parameters
    ----------
    path: PathLike
        path to the folder containing the DICOM slices. The folder should contain the DICOM slices,
        or a zip file named "dicom.zip" containing the DICOM slices.
    allow_raw_tags: bool
        Allow loading of any tags contained in DICOM, irrelevant of whether they are valid
    additional_tags: *str
        Load more strings than is defined in dicomselect.constants.
        A full list of all DICOM tags is available in dicomselect.tags_generated

    Usage
    -----
    >>> image = DICOMImageReader('path/to/dicom/folder').image

    or

    >>> reader = DICOMImageReader('path/to/dicom/folder')
    >>> image = reader.image
    >>> metadata = reader.metadata
    """

    def __init__(self, path: PathLike, verify_dicom_filenames: bool = False, allow_raw_tags: bool = True, additional_tags: list[str] = None):
        self._dcm_tags: List[DICOMTag] = DEFAULT_DICOM_TAGS
        if additional_tags:
            for tag in additional_tags:
                self._dcm_tags.append(DICOMTag(tag))

        self._path: Path = Path(path)
        self._allow_raw_tags = allow_raw_tags
        self._verify_dicom_filenames = verify_dicom_filenames
        self._is_zip = self._path.suffix == '.zip'

        self._image = None
        self._metadata = {}
        self._dicom_slice_paths: Optional[List[str]] = None
        self._series_reader = sitk.ImageSeriesReader()
        self._initialized = False

    def __len__(self) -> int:
        self._initialize()
        return len(self._dicom_slice_paths)

    def clear(self):
        self._image = None
        self._metadata = {}
        self._initialized = False

    @property
    def is_zipfile(self) -> bool:
        return self._is_zip

    @property
    def path(self) -> Path:
        return self._path

    @property
    def image(self) -> sitk.Image:
        self._initialize()
        if self._image is None:
            path = Path(self._path)
            if self.is_zipfile:
                with zipfile.ZipFile(path) as zf:
                    if not zf.namelist():
                        raise RuntimeError('zip file is empty')
                    with tempfile.TemporaryDirectory() as tempdir:
                        zf.extractall(tempdir)
                        self._image = self._read_image(path=tempdir)
            else:
                self._image = self._read_image(path=path)
        return self._image

    @property
    def metadata(self) -> Dict[str, str]:
        self._initialize()
        return self._get_metadata()

    def column_info(self):
        columns = {tag.name: tag.column_type for tag in self._dcm_tags}
        for key in self.metadata.keys():
            if key not in columns:
                columns[key] = "TEXT"
        return columns

    def _initialize(self):
        if not self._initialized:
            if self.is_zipfile:
                with zipfile.ZipFile(self._path, 'r') as zf:
                    self._dicom_slice_paths = [
                        self._path / name
                        for name in zf.namelist()
                        if name.endswith(".dcm")
                    ]
                if self._verify_dicom_filenames:
                    self._verify_dicom_filenames_func()
            else:
                self._set_dicom_list()
        self._initialized = True

    def _verify_dicom_filenames_func(self, filenames: Optional[List[PathLike]] = None) -> bool:
        """
        Verify DICOM filenames have increasing numbers, with no gaps

        Common prefixes are removed from the filenames before checking the numbers,
        this allows to verify filenames like "1.2.86.1.dcm", ..., "1.2.86.12.dcm".
        """
        if filenames is None:
            filenames = [os.path.basename(dcm) for dcm in self._dicom_slice_paths]

        # remove common prefixes
        common_prefix = os.path.commonprefix(filenames)
        if common_prefix:
            filenames = [fn.replace(common_prefix, "") for fn in filenames]
        common_postfix = os.path.commonprefix([fn[::-1] for fn in filenames])[::-1]
        if common_postfix:
            filenames = [fn.replace(common_postfix, "") for fn in filenames]

        # extract numbers from filenames
        filename_digits = [(''.join(c for c in str(fn) if c.isdigit())) for fn in filenames]
        filename_digits = [int(d) for d in filename_digits if d]
        if len(filename_digits) < 2:
            # either no numbers in the filenames, or only one file
            return True

        missing_slices = False
        for num in range(min(filename_digits), max(filename_digits) + 1):
            if num not in filename_digits:
                missing_slices = True
                break
        if missing_slices:
            raise MissingDICOMFilesError(self._path)
        return True

    def _set_dicom_list(self, path: Optional[PathLike] = None) -> None:
        """
        Set the list of paths to the DICOM slices.

        Parameters
        ----------
        path: PathLike
            path to the folder containing the DICOM slices. The folder should contain the DICOM slices,
            or a zip file containing the DICOM slices.
            default: self.path
        """
        if path is None:
            path = self._path

        self._dicom_slice_paths = self._series_reader.GetGDCMSeriesFileNames(str(path))

        # verify DICOM files are found
        if len(self._dicom_slice_paths) == 0:
            raise MissingDICOMFilesError(self._path)

        if self._verify_dicom_filenames:
            self._verify_dicom_filenames_func()

    def _read_image(self, index: int = 0, path: Optional[PathLike] = None) -> sitk.Image:
        if path is None:
            path = self._path
        path = Path(path)

        try:
            return self._read_image_sitk(index=index, path=path)
        except RuntimeError:
            # try again with pydicom
            return self._read_image_pydicom(index=index, path=path)

    def _read_image_sitk(self, index: int = 0, path: Optional[PathLike] = None) -> sitk.Image:
        """
        Read image using SimpleITK.

        Parameters
        ----------
        path: PathLike
            path to the folder containing the DICOM slices. The folder should contain the DICOM slices,
            or a zip file containing the DICOM slices.
            default: self.path

        Returns
        -------
        image: SimpleITK.Image
        """
        if path is not None:
            self._path = path
            self._set_dicom_list(path=path)

        # read DICOM sequence
        try:
            self._series_reader.SetFileNames(self._dicom_slice_paths)
            image: sitk.Image = self._series_reader.Execute()
        except RuntimeError:
            # try again while removing localizer slices
            self._dicom_slice_paths = filter_localizer_slices(self._dicom_slice_paths)
            self._series_reader.SetFileNames(self._dicom_slice_paths)
            image: sitk.Image = self._series_reader.Execute()

        # read metadata from the last DICOM slice
        reader = sitk.ImageFileReader()
        reader.SetFileName(self._dicom_slice_paths[index])
        reader.LoadPrivateTagsOn()
        reader.ReadImageInformation()

        # set metadata
        metadata = {key: reader.GetMetaData(key).strip() for key in reader.GetMetaDataKeys()}
        for key, value in metadata.items():
            if len(value) > 0:
                image.SetMetaData(key, value)

        return image

    def _read_image_pydicom(self, index: int = 0, path: Optional[PathLike] = None) -> sitk.Image:
        """
        Read image using pydicom. Warning: experimental! This function has limited capabilities.

        Parameters
        ----------
        path: PathLike
            path to the folder containing the DICOM slices. The folder should contain the DICOM slices,
            or a zip file containing the DICOM slices.
            default: self.path

        Returns
        -------
        image: SimpleITK.Image
        """
        if path is not None:
            self._path = path
            self._set_dicom_list(path=path)

        files = [pydicom.dcmread(dcm) for dcm in self._dicom_slice_paths]

        # skip files with no SliceLocation (eg. scout views)
        slices = filter(lambda a: hasattr(a, 'SliceLocation'), files)
        slices = sorted(slices, key=lambda s: s.SliceLocation)

        # create and fill 3D array
        image = np.zeros([len(slices)] + list(slices[0].pixel_array.shape))
        for index, s in enumerate(slices):
            image[index, :, :] = s.pixel_array

        # convert to SimpleITK
        image: sitk.Image = sitk.GetImageFromArray(image)
        ref = slices[index]  # corresponds to the same slice as with SimpleITK
        image.SetSpacing(list(ref.PixelSpacing) + [ref.SliceThickness])
        image.SetOrigin(ref.ImagePositionPatient)
        image.SetDirection(tuple(get_orientation_matrix(ref).transpose().flatten()))

        for key in ref.keys():
            # collect all available metadata (with DICOM tags, e.g. 0010|1010, as keys)
            value = get_pydicom_value(ref, key)
            if value is not None:
                key = str(key).replace(", ", "|").replace("(", "").replace(")", "")
                image.SetMetaData(key, value)

        return image

    def _get_metadata(self, index: int = 0) -> Dict[str, str]:
        if index < 0 or index >= len(self):
            raise IndexError(f"Index {index} out of range")
        if index in self._metadata:
            return self._metadata[index]

        # Read metadata from DICOM file
        metadata = self._read_metadata(index)

        uid_str = '_'.join([str(metadata[tag.name]) for tag in DEFAULT_DICOM_TAGS])
        metadata['dicomselect_uid'] = hashlib.blake2b(uid_str.encode(), digest_size=32).hexdigest()
        metadata["series_length"] = str(len(self))

        self._metadata[index] = metadata
        return metadata

    def _read_metadata(self, index: int = 0) -> Dict[str, str]:
        if self._image is not None and index == 0:
            return self._collect_metadata_sitk(self._image)

        if self.is_zipfile:
            # read metadata from dicom.zip with pydicom
            with zipfile.ZipFile(self._path) as zf:
                if not zf.namelist():
                    raise RuntimeError('zip file is empty')

                with tempfile.TemporaryDirectory() as tempdir:
                    targetpath = zf.extract(member=zf.namelist()[-1-index], path=tempdir)
                    return self._read_metadata_from_file(targetpath)

        # extract metadata from specified DICOM slice
        dicom_slice_path = self._dicom_slice_paths[index]
        return self._read_metadata_from_file(dicom_slice_path)

    def _read_metadata_from_file(self, path: PathLike) -> Dict[str, str]:
        try:
            reader = sitk.ImageFileReader()
            reader.SetFileName(str(path))
            reader.LoadPrivateTagsOn()
            reader.ReadImageInformation()
            return self._collect_metadata_sitk(reader)
        except Exception:
            try:
                with pydicom.dcmread(path, stop_before_pixels=True) as ds:
                    return self._collect_metadata_pydicom(ds)
            except pydicom.errors.InvalidDicomError:
                raise UnreadableDICOMError(path)

    def _collect_metadata_sitk(self, ref: Union[sitk.Image, sitk.ImageFileReader]) -> Dict[str, str]:
        metadata = {}
        for tag in self._dcm_tags:
            # collect metadata with DICOM names, e.g. patientsage, as keys)
            metadata[tag.name] = tag.convert(ref.GetMetaData(tag.key.lower()).strip() if ref.HasMetaDataKey(tag.key) else '')
        if self._allow_raw_tags:
            for key in ref.GetMetaDataKeys():
                # collect all available metadata (with DICOM tags, e.g. 0010|1010, as keys)
                try:
                    tag = DICOMTag(key)
                    if tag not in self._dcm_tags:
                        metadata[tag.name] = tag.convert(ref.GetMetaData(tag.key).strip())
                except InvalidTagError:
                    continue

        metadata["spacing_in_plane"] = str(ref.GetSpacing()[0:2])
        metadata["image_direction"] = get_orientation(ref.GetDirection())

        return metadata

    def _collect_metadata_pydicom(self, ds: "pydicom.dataset.Dataset") -> Dict[str, str]:
        metadata = {}
        for tag in self._dcm_tags:
            # collect metadata with DICOM names, e.g. patients_age, as keys)
            value = get_pydicom_value(ds, tag.key)
            metadata[tag.name] = tag.convert(value if value is not None else '')
        if self._allow_raw_tags:
            for key in ds.keys():
                # collect all available metadata (with DICOM tags, e.g. 0010|1010, as keys)
                tag = DICOMTag('|'.join([str(x).zfill(4) for x in [key.group, key.elem]]))
                if tag not in self._dcm_tags:
                    value = get_pydicom_value(ds, tag.key)
                    if value is not None:
                        metadata[tag.name] = tag.convert(value)

        metadata["spacing_in_plane"] = str(ds.PixelSpacing[0:2])
        metadata["image_direction"] = get_orientation([])
        return metadata

    def __repr__(self) -> str:
        return f'DICOMImageReader({self._path})'
