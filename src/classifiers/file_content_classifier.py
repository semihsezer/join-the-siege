

class FileContentClassifier:
    def __init__(self, text: str):
        self.text = text

    def classify(self) -> str:
        return "unknown"