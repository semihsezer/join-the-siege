from functools import cached_property
from .classifications import FileClassification

KEYWORD_MAP = {
    FileClassification.DRIVERS_LICENCE: {"driver", "license", "dl"},
    FileClassification.BANK_STATEMENT: {"bank", "statement"},
    FileClassification.INVOICE: {"invoice", "bill"},
}

class FileNameClassifier:
    """Classifies a file based on its filename and expected keywords in the tokens.

    Attempts to classify based on keyword matching to:
    - tokens
    - lemmas
    - and lemmas with corrected spelling
    """
    def __init__(self, filename: str):
        self.filename = filename

    @cached_property
    def cleaned_filename(self) -> str:
        """Replaces all non-alphanumeric characters with spaces and converts to lowercase."""
        import re
        return re.sub(r'[^a-zA-Z0-9]', ' ', self.filename.lower())

    @cached_property
    def tokens(self) -> list[str]:
        """Tokenizes the cleaned filename."""
        from nltk import download
        from nltk.tokenize import word_tokenize
        download("punkt_tab")

        return word_tokenize(self.cleaned_filename)

    @cached_property
    def lemmas(self) -> list[str]:
        """Lemmatizes the tokens."""
        from nltk import download
        from nltk.stem import WordNetLemmatizer
        download('wordnet')

        lemmatizer = WordNetLemmatizer()
        return [lemmatizer.lemmatize(token) for token in self.tokens]

    @cached_property
    def corrected_lemmas(self) -> list[str]:
        """Returns lemmas with spelling correction."""
        from autocorrect import Speller

        correct = Speller(lang='en')
        return [correct(lemma) for lemma in self.lemmas]

    def classify(self) -> FileClassification:
        for category, keywords in KEYWORD_MAP.items():
            # Try matching to tokens first
            if any(keyword in self.tokens for keyword in keywords):
                return category

            # If not, try matching to lemmas
            if any(keyword in self.lemmas for keyword in keywords):
                return category

            # If not, try matching to lemmas with corrected spelling
            if any(keyword in self.corrected_lemmas for keyword in keywords):
                return category

        return FileClassification.UNKNOWN