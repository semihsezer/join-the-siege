import pytest
from src.extractors.image_text_extractor import ImageTextExtractor


class TestImageTextExtractor:
    @pytest.mark.parametrize(
        "image_path,expected_keywords",
        [
            ("files/drivers_license/drivers_license_1.jpg", ["driver", "license"]),
            ("files/drivers_license/drivers_licence_2.jpg", ["driving", "licence"]),
            ("files/drivers_license/drivers_license_3.jpg", ["driver", "license"]),
        ],
    )
    def test_extract(self, image_path, expected_keywords):
        extractor = ImageTextExtractor(image_path)
        extractor.extract()
        extractor.clean()
        assert extractor.raw_text is not None
        assert extractor.cleaned_text is not None
        for keyword in expected_keywords:
            assert keyword in extractor.raw_text.lower()

        assert len(extractor.cleaned_text) > 0

    def test_unsupported_file_type(self):
        with pytest.raises(ValueError, match=".*Unsupported.*type.*"):
            ImageTextExtractor("x/drivers_license_1.unknown")
