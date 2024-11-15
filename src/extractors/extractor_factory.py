from src.extractors.file_types import FileType
from src.extractors.base_text_extractor import BaseTextExtractor
from src.extractors.image_text_extractor import ImageTextExtractor
from src.extractors.pdf_text_extractor import PDFTextExtractor


def get_extractor(file_path: FileType, convert_pdf_to_image=False) -> 'BaseTextExtractor':
    """Returns an extractor instance based on the given file's path and extension.

    :param file_path: :str Path to the file to extract text from.
    :param convert_pdf_to_image: :bool Whether to convert a PDF to image first and
        extract text with OCR rather than PDF parser. Default is False.

    :returns: :BaseTextExtractor An instance of the appropriate text extractor.
    """
    file_type: FileType = FileType.from_file_path(file_path)
    if file_type in ImageTextExtractor.supported_file_types():
        return ImageTextExtractor(file_path)
    elif file_type in PDFTextExtractor.supported_file_types():
        return PDFTextExtractor(file_path, convert_pdf_to_image=convert_pdf_to_image)
    else:
        raise ValueError(f"Unsupported file type: {file_type}. "
                         f"Has to be one of: {FileType}, "
                         f"{PDFTextExtractor.supported_file_types()}. "
                         f"File path: {file_path}"
                         )