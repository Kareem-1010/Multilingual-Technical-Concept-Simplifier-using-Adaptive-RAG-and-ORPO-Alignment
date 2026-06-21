from langdetect import detect, LangDetectException
from config import SUPPORTED_LANGUAGES

class LanguageDetector:
    def detect(self, text: str) -> str:
        try:
            code = detect(text)
            if code in SUPPORTED_LANGUAGES:
                return code
            return "en" # Fallback if unsupported
        except LangDetectException:
            return "en" # Fallback if detection fails

    def get_display_name(self, code: str) -> str:
        return SUPPORTED_LANGUAGES.get(code, "English")
