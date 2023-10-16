import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable, Dict, List, Optional, Union

import SimpleITK as sitk
from tqdm import tqdm
from treelib import Tree

from dicomselect.reader import DICOMImageReader
from dicomselect.logging import Logger, LOG_FILENAME

CustomPostprocessFunction = Callable[[DICOMImageReader], Union[sitk.Image, Dict[str, sitk.Image]]]


class Convert:
    def __init__(self, uid: str, source: str, target: str, columns: List[str], values: List[str]):
        if len(columns) != len(values):
            raise RuntimeError()

        self.uid = uid
        self.source = Path(source)
        for col, value in set(zip(columns, values)):
            target = self._column_replace_sanitize(target, col, value)
        self.target = Path(target)

    # noinspection RegExpRedundantEscape
    @staticmethod
    def _column_replace_sanitize(text: str, col: str, value):
        placeholder = '{' + col + '}'
        value = str(value)
        # no non-printable characters
        value = re.sub(r'[\x00-\x1F]', '☒', value)
        # forbidden ascii characters
        value = re.sub(r'[<>:"\/\\\|\?\*]', '#', value)
        # may not end with a dot or space
        value = re.sub(r'[\. ]+$', '', value)
        # if the result is empty, return [col]=blank instead
        if len(value) == 0:
            return text.replace(placeholder, f'empty_{col}')
        return text.replace(placeholder, value)

    def __str__(self):
        return f'{self.source} -> {self.target}'

    def convert(self, extension: str, source_dir: Path, target_dir: Path,
                postprocess_func: Optional[CustomPostprocessFunction] = None) -> str:
        reader = DICOMImageReader(source_dir / self.source)

        if postprocess_func:
            try:
                return_value = postprocess_func(reader)
                msg = f'PostProcessFunction did not return an Image or a Dict[str, Image] ({str(self)})'

                if return_value is None or not return_value:
                    return
                elif isinstance(return_value, sitk.Image):
                    convert_dict: Dict[str, sitk.Image] = {'': return_value}
                elif isinstance(return_value, dict):
                    for key, image in return_value.items():
                        assert isinstance(key, str), ValueError(msg)
                        assert isinstance(image, sitk.Image), ValueError(msg)
                    convert_dict: Dict[str, sitk.Image] = return_value
                else:
                    raise ValueError(msg)
            except Exception as e:
                raise e
        else:
            convert_dict: Dict[str, sitk.Image] = {'': reader.image}

        for suffix, image in convert_dict.items():
            name = str(self.target) + suffix + extension
            target = target_dir / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target_tmp = target.parent / ('tmp_' + target.name)
            sitk.WriteImage(image, target_tmp.as_posix(), useCompression=True)
            os.replace(target_tmp, target)


class Plan(Logger):
    def __init__(self, default_source_dir: Path, converts: List[Convert]):
        super().__init__()
        self._converts = converts

        self._source_dir = default_source_dir
        self._extension = '.mha'
        self._target_dir: Path = None

        self._missing: List[Path] = []
        self._invalidated = True

    def _invalidate(self, attr: str, value):
        if getattr(self, attr) != value:
            self._invalidated = True

    @property
    def source_dir(self) -> Path:
        """
        Source directory, containing your data that is to be converted.
        """
        return self._source_dir

    @source_dir.setter
    def source_dir(self, value: os.PathLike):
        value = Path(value).absolute()
        assert value.exists() and value.is_dir(), NotADirectoryError(f'{value} is not a directory.')
        self._invalidate('source_dir', value)
        self._source_dir = value

    @property
    def target_dir(self) -> Path:
        """
        Target directory, to contain the converted data.
        """
        return self._target_dir

    @target_dir.setter
    def target_dir(self, value: os.PathLike):
        assert value is not None, ValueError('target_dir is not set.')
        value = Path(value).absolute()
        assert not value.exists() or value.is_dir(), NotADirectoryError(f'{value} is not a directory.')
        if value.exists():
            files = [file.name for file in value.iterdir()]
            assert len(files) == 0 or files == [LOG_FILENAME], ValueError(f'{value} is not empty.')
        self._invalidate('target_dir', value)
        self._target_dir = value

    @property
    def extension(self) -> str:
        """
        The extension defines the converted filetype. See https://simpleitk.readthedocs.io/en/master/IO.html#images
        for possible file formats to convert to.
        """
        return self._extension

    @extension.setter
    def extension(self, value: str):
        assert value.startswith('.'), ValueError('extension must start with a period.')
        self._invalidate('extension', value)
        self._extension = value

    def _validate(self):
        if not self._invalidated:
            return

        self.source_dir = self._source_dir  # performs a validation of source dir
        self.target_dir = self._target_dir  # performs a validation of target dir

        self.init_logger(self.target_dir / LOG_FILENAME)

        sources: Dict[str, List[Convert]] = dict()
        targets: Dict[str, List[Convert]] = dict()
        for convert in tqdm(self._converts, desc="Validating conversion plan"):
            source, target = convert.source.as_posix(), convert.target.as_posix()
            sources[source] = sources.get(source, []) + [convert]
            targets[target] = targets.get(target, []) + [convert]
            if not (self.source_dir / convert.source).exists():
                self.log(f'Missing source file for {str(convert)}')

        for sourgets, txt in [(sources, 'sources'), (targets, 'targets')]:
            for key, converts in sourgets.items():
                if len(converts) > 1:
                    self.log(f'Duplicate {txt} found: (source -> target)\n' + '\n'.join([' ' * 33 + str(c) for c in converts]))

        if self.errors > 0:
            raise RuntimeError(f'{self.errors} errors during data validation: See {self.path_log} for details')

        self._invalidated = False

    def _tree(self) -> Tree:
        self._validate()

        tree = Tree()
        root = tree.create_node('.', Path('.'))
        for convert in self._converts:
            prev_parent = root
            path = Path(convert.target)
            for parent in path.parents:
                if parent not in tree:
                    tree.create_node(str(parent), parent, parent=prev_parent.identifier)
            tree.create_node(path.name + self.extension, path, parent=path.parent)

        return tree

    def to_string(self) -> str:
        """
        The conversion plan as a string, in a tree representation.

        Returns
        -------
        The representation.
        """
        self._validate()

        tree = self._tree()
        text = 'dicomselect conversion plan\n'
        for param in ['source_dir', 'target_dir', 'extension']:
            text += '\n' + f'{param:<20}{getattr(self, param)}'
        return text + '\n\n' + tree.show(stdout=False)

    def execute(self, max_workers: int = 4, postprocess_func: Optional[CustomPostprocessFunction] = None):
        """
        Execute the conversion plan.

        Parameters
        ----------
        max_workers
            Max number of workers for parallel execution of this conversion.
        postprocess_func:
            Postprocess function, providing a DICOMImageReader. If it returns False, the conversion is skipped. If it
            returns a SimpleITK.Image, the conversion is executed using the returned image. If it returns a dict of
            [str, SimpleITK.Image], it converts each entry, where key is attached to the end of the name template.
            Note that multiple converted files from one image will not be cached and will be marked for deletion in future
            plans due to the anonymous nature of this function.
        """
        self._validate()
        self.init_logger(self.target_dir / LOG_FILENAME)

        converts_len = len(self._converts)

        try:
            convert_args = (self.extension, self.source_dir, self.target_dir, postprocess_func)

            if not self.target_dir.exists():
                self.target_dir.mkdir(parents=True)

            def _execute(convert: Convert) -> Optional[str]:
                return convert.convert(*convert_args)

            print(f"Converting {converts_len} DICOM series from {self.source_dir} to {self.target_dir}")
            with tqdm(total=converts_len, desc=f"Converting to {self.extension}") as pbar, ThreadPoolExecutor(max_workers=max_workers) as pool:
                chunk_size = 5000
                for i in range(0, converts_len, chunk_size):
                    futures = {pool.submit(_execute, convert): convert for convert in self._converts[i:i+chunk_size]}
                    for future in as_completed(futures):
                        if exc := future.exception():
                            self.log(exc, Convert=futures[future])
                        pbar.update()
                        pbar.set_description(f'({self.errors} errors)')

            print(f"Conversion complete with {self.errors} errors.")
        finally:
            if self.errors > 0:
                print(f'{self.errors} errors during conversion: See {self.path_log} for details')

    def __str__(self) -> str:
        return self.to_string()
