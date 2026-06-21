
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import textstat
import re

# Download resources if not present
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

class TextPreprocessor:
    def __init__(self):
        pass
            
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def normalize(self, text: str) -> str:
        text = text.lower()
        # Remove special characters but keep spaces
        text = re.sub(r'[^\w\s]', '', text)
        return " ".join(text.split())

    def tokenize(self, text: str):
        import re
        return re.findall(r'\b\w+\b', text)

    def lemmatize(self, tokens: list) -> list:
        return [self.lemmatizer.lemmatize(token) for token in tokens]

    def remove_stopwords(self, tokens: list) -> list:
        return [token for token in tokens if token.lower() not in self.stop_words]

    def pos_tag(self, text: str) -> dict:
        return {"noun_phrases": [], "verb_groups": []}

    def ner(self, text: str) -> list:
        return []

    def readability_score(self, text: str) -> float:
        return textstat.flesch_reading_ease(text)

    def full_analysis(self, text: str) -> dict:
        normalized = self.normalize(text)
        tokens = self.tokenize(text)
        lemmas = self.lemmatize(tokens)
        clean_tokens = self.remove_stopwords(tokens)
        
        return {
            "original_text": text,
            "normalized": normalized,
            "tokens": tokens,
            "lemmas": lemmas,
            "clean_tokens": clean_tokens,
            "pos_tags": self.pos_tag(text),
            "entities": self.ner(text),
            "readability_score": self.readability_score(text)
        }
