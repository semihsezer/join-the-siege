from .perplexity_client import PerplexityClient

class FileContentClassifier:
    """Classifies files based on text content by using online LLMs."""
    def __init__(self):
        pass

    def classify(self, text:str, categories: set[str], max_chars=1000) -> str:
        """
        :param text: :str Text to classify into one of the categories.
        :param categories: :set[str] Set of categories to classify the text into.
        :param max_chars: :int Maximum number of characters to use for classification.

        :returns: :str Classification of the text into one of the categories.
        """
        perplexity = PerplexityClient()
        categories_part = ", ".join(categories)
        text_part = text[:max_chars]
        prompt = ("Classify the following text into one of these categories:\n"
                 f"categories: {categories_part}"
                 f"Your response should only include one of the categories above. Do not return anything else. Here is the text:\n"
                 f"{text_part}"
                 )

        classification = perplexity.generate(prompt)
        if classification not in categories:
            raise ValueError(f"Perplexity returned more than just the classification: {classification}")
        return classification