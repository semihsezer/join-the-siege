import abc
from pathlib import Path


class BaseTextExtractor(abc.ABC):
    """Abstract base class for text extractors."""
    SUPPORTED_FILE_TYPES = {}

    def validate_file(self, file_path: str):
        """Validates file.
        """
        file_type = file_path.split(".")[-1].lower()
        if file_type not in self.supported_file_types():
            raise ValueError(
                f"Unsupported file type: {file_type}. "
                "Has to be one of: {self.SUPPORTED_FILE_TYPES}."
            )

    def validate_extracted(self, text):
        """Validates extrated text.

        :raises ValueError if no text was extracted.
        """
        if not text:
            raise ValueError(
                "No text was extracted. Either there is no text or extraction failed."
            )

    @classmethod
    def supported_file_types(self) -> set[str]:
        """Returns a set of supported file type extensions ie. pdf, docx, jpg."""
        return self.SUPPORTED_FILE_TYPES

    @abc.abstractmethod
    def extract(self, file_path: str) -> str:
        """Extracts text data from the file.

        :param file_path: Path to the file to extract text from.
        :returns :str Extracted text.
        """
        pass
