from enum import StrEnum

class FileType(StrEnum):
    PDF = "pdf"
    PNG = "png"
    JPG = "jpg"
    JPEG = "jpeg"

    @classmethod
    def from_file_path(cls, file_path: str):
        """Returns the FileType based on the file path."""
        file_type = file_path.split(".")[-1]
        return cls(file_type)
