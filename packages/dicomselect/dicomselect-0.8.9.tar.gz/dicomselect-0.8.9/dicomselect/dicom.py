import re
from typing import Callable

from dicomselect.constants import DEFAULT_DICOM_TAGS
from dicomselect.tags_generated import tags_generated, version


class InvalidTagError(ValueError):
    pass


class DICOMTag:
    def __init__(self, tag: str):
        r = re.search(r'(.{4})[,| ]+(.{4})', tag.upper())
        if not r:
            raise InvalidTagError(f'Invalid tag, could not parse {tag}')
        self._tag = r.groups()

        from_generated_tags = tags_generated.get(self.key.upper(), None)
        if from_generated_tags is None:
            raise InvalidTagError(f'Invalid tag, does not exist in {version}')

        self._name = from_generated_tags[0]
        vr = VR.get(from_generated_tags[1], "TEXT")
        if isinstance(vr, str):
            # "TEXT", "REAL" or "INTEGER", encode.decode deals with invalid characters
            vr = (vr, lambda v: v.encode(errors='ignore').decode(errors='ignore'))

        self._datatype = vr[0]
        self._convert_func: Callable[[str], str] = vr[1]

    def __eq__(self, other):
        if isinstance(other, DICOMTag):
            return self.key == other.key
        return False

    @property
    def name(self) -> str:
        return re.sub(r'\W+', '', self._name.replace(' ', '_')).lower()

    @property
    def key(self) -> str:
        return f'{self._tag[0]}|{self._tag[1]}'.lower()

    @property
    def column_type(self) -> str:
        return self._datatype

    def convert(self, value: str):
        return self._convert_func(value) if value else ''

    def __repr__(self):
        return f'{self.key} {self.name} {self.column_type}'


def convert_AS(value: str):
    t = value[3]
    value = int(value[:3])
    if t == 'D':
        value /= 365
    elif t == 'M':
        value /= 12
    elif t == 'W':
        value /= 52
    return value


def convert_DT(value: str):
    value = value.replace(' ', '')
    r = re.search(r'^(\d{14}).?(\d+)?', value)
    return r.group()


# https://dicom.nema.org/medical/dicom/current/output/chtml/part05/sect_6.2.html
VR = {
    "AS": ("REAL", convert_AS),
    "DA": "INTEGER",
    "DT": ("REAL", convert_DT),
    "DS": "REAL",
    "FL": "REAL",
    "FD": "REAL",
    "IS": "INTEGER",
    "SL": "INTEGER",
    "SS": "INTEGER",
    "TM": "REAL",
    "UL": "INTEGER",
    "US": "INTEGER"
}


DEFAULT_DICOM_TAGS = [DICOMTag(tag) for tag in DEFAULT_DICOM_TAGS]
