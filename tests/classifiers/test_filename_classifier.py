import pytest
from src.classifier import FileNameClassifier, FileClassification

C = FileClassification

class TestImageTextExtractor:
    @pytest.mark.parametrize(
        "filename,expected_classification",
        [
            ("bank_statement_1.pdf", C.BANK_STATEMENT),
            ("invoice_1.pdf", C.INVOICE),
            ("drivers_license_1.jpg", C.DRIVERS_LICENCE),
        ]
    )
    def test_classify(self, filename, expected_classification):
        classifier = FileNameClassifier(filename)
        classification = classifier.classify()
        assert classification == expected_classification

    @pytest.mark.parametrize(
        "filename,expected_classification",
        [
            ("bank_statemnt_1.pdf", C.BANK_STATEMENT),
            ("bnk_statemnt_1.pdf", C.BANK_STATEMENT),
            ("drivers_licence_2.jpg", C.DRIVERS_LICENCE),
            ("drver_license_2.jpg", C.DRIVERS_LICENCE),
            ("driver_lcense_2.jpg", C.DRIVERS_LICENCE),
        ]
    )
    def test_classify_misspelled(self, filename, expected_classification):
        classifier = FileNameClassifier(filename)
        classification = classifier.classify()
        assert classification == expected_classification
