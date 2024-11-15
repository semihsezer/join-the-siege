import pytest
from src.extractors.image_text_extractor import ImageTextExtractor


class TestImageTextExtractor:
    @pytest.mark.parametrize(
        "image_path,expected_keywords",
        [
            ("files/raw/drivers_license/drivers_license_1.jpg", ["driver", "license"]),
            ("files/raw/drivers_license/drivers_licence_2.jpg", ["driving", "licence"]),
            ("files/raw/drivers_license/drivers_license_3.jpg", ["driver", "license"]),
        ],
    )
    def test_extract(self, image_path, expected_keywords):
        extractor = ImageTextExtractor(image_path)
        text = extractor.extract()
        assert text is not None
        for keyword in expected_keywords:
            assert keyword in text.lower()

    def test_unsupported_file_type(self):
        with pytest.raises(ValueError, match=".*Unsupported.*type.*"):
            ImageTextExtractor("x/drivers_license_1.unknown")
