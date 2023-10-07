import mimetypes
from abc import ABC
from pathlib import Path
from typing import Optional

from pydantic import Extra, Field, root_validator, validator

from kognic.io.model.base_serializer import BaseSerializer
from kognic.io.resources.scene.file_data import FileData


class MissingFileError(BaseException):
    filename: str
    empty: bool

    def __init__(self, filename: str, empty: bool = False):
        self.filename = filename
        self.empty = empty

    def to_string(self):
        return f"Local file {self.empty and 'contains no data' or 'is missing'}: {self.filename}"


class Resource(ABC, BaseSerializer):
    filename: str
    resource_id: Optional[str] = None
    sensor_name: str
    file_data: Optional[FileData] = Field(default=None, exclude=True)
    client_filename: Optional[str]

    class Config(BaseSerializer.Config):
        arbitrary_types_allowed = {"file_data": True}
        extra = Extra.forbid

    @property
    def content_type(self):
        if self.file_data:
            return self.file_data.content_type
        content_type = mimetypes.guess_type(self.filename)[0]
        return content_type if content_type is not None else "application/octet-stream"

    @root_validator(pre=True)
    def check_filename(cls, v):
        if v.get("file_data") is None:
            filename = v.get("filename")
            path = Path(filename)
            if not path.exists():
                raise MissingFileError(filename)
            if not path.stat().st_size > 0:
                raise MissingFileError(filename, empty=True)
        return v

    @root_validator(pre=True)
    def check_source_of_data(cls, values):
        filename = values.get("filename")
        resource_id = values.get("resource_id")
        file_data = values.get("file_data")
        values["client_filename"] = filename
        filename_path = Resource.filename_path(filename, file_data)
        values["filename"] = str(filename_path)
        if resource_id is None:
            values["resource_id"] = Resource.resource_id_from_filename(filename_path)
        return values

    @staticmethod
    def filename_path(filename: str, file_data: FileData):
        return Resource.suffix_for_data(Path(filename).expanduser(), file_data)

    @staticmethod
    def suffix_for_data(path: Path, file_data: FileData) -> Path:
        if file_data is None:
            return path
        return path if path.suffix == file_data.suffix else path.with_name(path.stem + path.suffix + file_data.suffix)

    @staticmethod
    def resource_id_from_filename(filename_path: Path) -> str:
        """
        Protects against cloud storage limitation of one period per resource by replacing any others.
        """
        path = filename_path
        filename = path.name
        if "." in filename:
            path = path.with_name(filename.replace(".", "_", filename.count(".") - 1))
        return str(path)
