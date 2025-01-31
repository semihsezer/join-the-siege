from datetime import time
from enum import StrEnum
from tempfile import NamedTemporaryFile
from werkzeug.datastructures import FileStorage
from flask import request

from .classifiers import FileClassification, FileContentClassifier, FileNameClassifier
from .extractors import get_extractor
import logging


logging.basicConfig(level=logging.INFO)

class ClassificationCategory(StrEnum):
    BANK_STATEMENT = "bank_statement"
    INVOICE = "invoice"
    DRIVERS_LICENSE = "drivers_license"
    UNKNOWN = "unknown"

class ClassifierType(StrEnum):
    FILENAME = "filename_classifier"
    CONTENT = "content_classifier"


def classify_file(file: FileStorage, classifier=ClassifierType.CONTENT,
                  convert_pdf_to_image=False) -> FileClassification:
    logging.info(f"Classifying: {file.filename}. Options: classifier: {classifier}, "
                 f"convert_pdf_to_image: {convert_pdf_to_image}")

    if classifier == ClassifierType.FILENAME:
        classifier = FileNameClassifier(file.filename)
        classification = classifier.classify()
    else:
        temp_file = NamedTemporaryFile(delete=False, suffix=file.filename)
        temp_file.write(file.read())
        temp_file.flush()

        extractor = get_extractor(temp_file.name, convert_pdf_to_image=convert_pdf_to_image)
        text = extractor.extract()
        categories = {category for category in ClassificationCategory}
        classifier = FileContentClassifier()
        classification = classifier.classify(text, categories)

    return classification
