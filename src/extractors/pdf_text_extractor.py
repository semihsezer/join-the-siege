from enum import StrEnum
from tempfile import NamedTemporaryFile
from src.extractors.base_text_extractor import BaseTextExtractor

class PDFModule(StrEnum):
    PDF2IMAGE = "pdf2image"
    PYMUPDF = "pymupdf"


class PDFTextExtractor(BaseTextExtractor):
    """Extracts text data from PDF files."""
    SUPPORTED_FILE_TYPES = {"pdf"}

    def __init__(self,
                 file_path: str,
                 module: PDFModule = PDFModule.PYMUPDF):
        super().__init__(file_path)
        self.validate()
        self.module = module

    @property
    def supported_file_types(self):
        return self.SUPPORTED_FILE_TYPES

    def clean(self) -> list[str]:
        if not self.raw_text:
            raise ValueError("No text was extracted. Run extract method first.")
        self.cleaned_text = [
            line.split(" ") for line in self.raw_text.split("\n") if line
        ]
        return self.cleaned_text

    def extract_via_pymupdf(self) -> str:
        import pymupdf

        pdf = pymupdf.open(self.file_path)
        text = ""
        for page in pdf:
            text += page.get_text() + "\n\n"

        return text

    def extract_via_image_conversion(self, first_page_only=False) -> str:
        """Extracts text from PDF files by converting them to images first and then using OCR.

        :param first_page_only: If True, only extracts text from the first page.
        """
        from src.extractors.image_text_extractor import ImageTextExtractor
        from pdf2image import convert_from_path

        pages = convert_from_path(self.file_path, 200)
        if first_page_only:
            pages = pages[:1]

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
        """Extracts text data from the PDF file."""
        if self.module == PDFModule.PDF2IMAGE:
            self.raw_text = self.extract_via_image_conversion(first_page_only=True)
        elif self.module == PDFModule.PYMUPDF:
            self.raw_text = self.extract_via_pymupdf()
        else:
            raise ValueError(f"Unsupported PDF extraction module: {self.module}")

        self.validate_extracted()

        return self.raw_text