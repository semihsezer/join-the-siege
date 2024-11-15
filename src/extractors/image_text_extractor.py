from src.extractors.base_text_extractor import BaseTextExtractor
from .file_types import FileType

class ImageTextExtractor(BaseTextExtractor):
    """Extracts text data from images."""

    SUPPORTED_FILE_TYPES = {FileType.PNG, FileType.JPG, FileType.JPEG}

    def __init__(self, file_path: str, **kwargs):
        self.file_path = file_path
        self.validate_file(file_path)

        # OCR Engine Mode and Page Segmentation Mode
        self.ocr_config = r"--oem 3 --psm 12"

    def extract(self) -> str:
        import cv2
        import pytesseract

        image = cv2.imread(self.file_path)
        if image is None:
            raise ValueError(f"Could not read image: {self.file_path}")

        # Convert the image to grayscale and apply thresholding
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        text = pytesseract.image_to_string(thresh, config=self.ocr_config)
        self.validate_extracted(text)

        return text
