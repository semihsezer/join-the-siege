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

    @property
    def file_type(self):
        return self.file_path.split(".")[-1]

    def validate(self):
        if self.file_type not in self.supported_file_types:
            raise ValueError(
                f"Unsupported file type: {self.file_type}. "
                "Has to be one of: {self.SUPPORTED_FILE_TYPES}. "
                "File path: {self.file_path}"
            )
        if not Path(self.file_path).exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")

    def validate_extracted(self):
        """Validates extrated text.

        :raises ValueError if no text was extracted.
        """
        if not self.raw_text:
            raise ValueError(
                "No text was extracted. Either there is no text or extraction failed."
            )

    @property
    @abc.abstractmethod
    def supported_file_types(self) -> set[str]:
        """Returns a set of supported file type extensions ie. pdf, docx, jpg."""
        pass

    @abc.abstractmethod
    def clean(self):
        """Cleans the raw text extracted from the file."""
        pass

    @abc.abstractmethod
    def extract(self, file_path: str):
        """Extracts text data from the file."""
        pass
