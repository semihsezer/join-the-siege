import abc
from pathlib import Path


class BaseTextExtractor(abc.ABC):
    """Abstract base class for text extractors."""
    def __init__(self, file_path: str):
        """
        :param file_path: Path to the file to extract text from.
        """
        self.file_path = file_path
        self.raw_text: str = None
        self.cleaned_text: list[str] = None

    def validate(self):
        file_type = self.file_path.split(".")[-1]
        if file_type not in self.supported_file_types:
            raise ValueError(f"Unsupported image file type: {self.file_type}. "
                             "Has to be one of: {self.SUPPORTED_FILE_TYPES}. "
                             "Image Path: {self.file_path}"
                             )
        if not Path(self.file_path).exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")

    @property
    @abc.abstractmethod
    def supported_file_types(self) -> set[str]:
        """Returns a set of supported file type extensions ie. .pdf, .docx, .jpg."""
        pass

    @abc.abstractmethod
    def clean(self):
        """Cleans the raw text extracted from the file."""
        pass

    @abc.abstractmethod
    def extract(self, file_path: str):
        """Extracts text data from the file."""
        pass
