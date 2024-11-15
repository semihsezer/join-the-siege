from enum import StrEnum
from tempfile import NamedTemporaryFile
from src.extractors.base_text_extractor import BaseTextExtractor
from src.extractors.file_types import FileType
import logging


logging.basicConfig(level=logging.INFO)


class PDFTextExtractor(BaseTextExtractor):
    """Extracts text data from PDF files."""
    SUPPORTED_FILE_TYPES = {FileType.PDF}

    def __init__(self, file_path:str, convert_pdf_to_image: bool = False):
        """
        :param file_path: :str Path to the PDF file to extract text from.
        :param convert_pdf_to_image: :bool Optional Whether to convert the PDF to image first and
            extract text with OCR rather than PDF parser. This will be slower but
            more accurate with poorly formatted PDFs or scanned documents.
            Default is False.
        """
        self.file_path = file_path
        self.convert_pdf_to_image = convert_pdf_to_image
        self.validate_file(file_path)

    def extract_via_pymupdf(self) -> str:
        import pymupdf

        pdf = pymupdf.open(self.file_path)
        text = ""
        for page in pdf:
            text += page.get_text() + "\n\n"

        return text

    def extract_via_image_conversion(self) -> str:
        from src.extractors.image_text_extractor import ImageTextExtractor
        from pdf2image import convert_from_path

        # Convert PDF to images
        pages = convert_from_path(self.file_path, dpi=200)

        # Extract text from images
        text = ""
        for page in pages:
            # NOTE: We could optimize by passing image directly rather than saving to disk
            file = NamedTemporaryFile(suffix=".png", delete=False)
            page.save(file.name, page.format)
            image_extractor = ImageTextExtractor(file.name)
            text += image_extractor.extract() + '\n\n'
        return text

    def extract(self) -> str:
        """Extracts text data from the PDF file.

        :param file_path: :str Path to the PDF file to extract text from.
        :returns: :str Extracted text data.
        """
        if self.convert_pdf_to_image:
            logging.info(f"Extracting text from PDF via image conversion. File Path: {self.file_path}")
            text = self.extract_via_image_conversion()
        else:
            logging.info(f"Extracting text from PDF via PDF Parser. File Path: {self.file_path}")
            text = self.extract_via_pymupdf()

        self.validate_extracted(text)
        return text