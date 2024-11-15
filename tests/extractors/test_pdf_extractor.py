import pytest
from src.extractors.pdf_text_extractor import PDFTextExtractor


class TestImageTextExtractor:
    @pytest.mark.parametrize(
        "image_path,expected_keywords",
        [
            ("files/raw/bank_statement/bank_statement_1.pdf", ["bank", "statement"]),
            ("files/raw/bank_statement/bank_statement_2.pdf", ["bank", "statement"]),
            ("files/raw/bank_statement/bank_statement_3.pdf", ["bank", "statement"]),
            ("files/raw/invoice/invoice_1.pdf", ["invoice", "quantity", "price"]),
            ("files/raw/invoice/invoice_2.pdf", ["invoice"]),
            ("files/raw/invoice/invoice_3.pdf", ["invoice", "rate"]),
        ],
    )
    def test_extract(self, image_path, expected_keywords):
        extractor = PDFTextExtractor(image_path,
                                     convert_pdf_to_image=False)
        text = extractor.extract()

        assert text is not None
        for keyword in expected_keywords:
            assert keyword in text.lower()

    @pytest.mark.parametrize(
        "image_path,expected_keywords",
        [
            ("files/raw/bank_statement/bank_statement_1.pdf", ["bank", "statement"]),
            ("files/raw/bank_statement/bank_statement_2.pdf", ["bank", "statement"]),
            ("files/raw/bank_statement/bank_statement_3.pdf", ["bank", "statement"]),
            ("files/raw/invoice/invoice_1.pdf", ["invoice", "quantity", "price"]),
            ("files/raw/invoice/invoice_2.pdf", ["invoice"]),
            ("files/raw/invoice/invoice_3.pdf", ["invoice", "rate"]),
        ],
    )
    def test_extract_via_image_conversion(self, image_path, expected_keywords):
        extractor = PDFTextExtractor(image_path,
                                     convert_pdf_to_image=True)
        text = extractor.extract()

        assert text is not None
        for keyword in expected_keywords:
            assert keyword in text.lower()

    def test_unsupported_file_type(self):
        with pytest.raises(ValueError, match=".*Unsupported.*type.*"):
            PDFTextExtractor("x/drivers_license_1.unknown")
