from tempfile import NamedTemporaryFile
import pytest
from src.extractors.extractor_factory import get_extractor

class TestGetExtractor:
    @pytest.mark.parametrize(
        "file_extension,expected_extractor",
        [
            (".pdf", "PDFTextExtractor"),
            (".png", "ImageTextExtractor"),
            (".jpg", "ImageTextExtractor"),
            (".jpeg", "ImageTextExtractor"),
        ]
    )
    def test_get_extractor(self, file_extension, expected_extractor):
        file = NamedTemporaryFile(delete=False, suffix=file_extension)
        extractor = get_extractor(file.name)
        assert extractor.__class__.__name__ == expected_extractor
        assert extractor.file_path == file.name

    def test_get_extractor_unsupported_file_type(self):
        file = NamedTemporaryFile(delete=False, suffix=".unknown")
        with pytest.raises(ValueError, match=".*unknown.*Type.*"):
            get_extractor(file.name)