import pytest
from src.extractors.pdf_text_extractor import PDFTextExtractor, PDFModule


class TestImageTextExtractor:
    @pytest.mark.parametrize(
        "image_path,expected_keywords",
        [
            ("files/bank_statement/bank_statement_1.pdf", ["bank", "statement"]),
            ("files/bank_statement/bank_statement_2.pdf", ["bank", "statement"]),
            ("files/bank_statement/bank_statement_3.pdf", ["bank", "statement"]),
            ("files/invoice/invoice_1.pdf", ["invoice", "quantity", "price"]),
            ("files/invoice/invoice_2.pdf", ["invoice"]),
            ("files/invoice/invoice_3.pdf", ["invoice", "rate"]),
        ],
    )
    def test_extract_bank_statements(self, image_path, expected_keywords):
        extractor = PDFTextExtractor(image_path,
                                     module=PDFModule.PYMUPDF)
        extractor.extract()
        extractor.clean()

        assert extractor.raw_text is not None
        assert extractor.cleaned_text is not None
        for keyword in expected_keywords:
            assert keyword in extractor.raw_text.lower()

        assert len(extractor.cleaned_text) > 0

    def test_unsupported_file_type(self):
        with pytest.raises(ValueError, match=".*Unsupported.*type.*"):
            PDFTextExtractor("x/drivers_license_1.unknown")
