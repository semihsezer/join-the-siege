from werkzeug.datastructures import FileStorage
from .classifiers.classifications import FileClassification
from .classifiers.filename_classifier import FileNameClassifier


def classify_file(file: FileStorage) -> FileClassification:
    filename = file.filename.lower()
    filename_classification = FileNameClassifier(filename).classify()
    return filename_classification

    # file_bytes = file.read()
