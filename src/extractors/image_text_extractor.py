from src.extractors.base_text_extractor import BaseTextExtractor


class ImageTextExtractor(BaseTextExtractor):
    """Extracts text data from images."""

    SUPPORTED_FILE_TYPES = {"png", "jpg", "jpeg"}

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.raw_text: str = None
        self.cleaned_text: list[str] = None

        # OCR Engine Mode and Page Segmentation Mode
        self.ocr_config = r"--oem 3 --psm 12"
        self.validate()

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

    def extract(self, raise_on_empty: bool = True) -> str:
        """
        :param raise_on_empty: If True, raises an error if no text was extracted.
        """
        import cv2
        import pytesseract

        image = cv2.imread(self.file_path)
        if image is None:
            raise ValueError(f"Could not read image: {self.file_path}")

        # Convert the image to grayscale and apply thresholding
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        self.raw_text = pytesseract.image_to_string(thresh, config=self.ocr_config)
        self.validate_extracted()

        return self.raw_text
