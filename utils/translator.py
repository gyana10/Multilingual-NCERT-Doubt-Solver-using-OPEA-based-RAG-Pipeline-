from langdetect import detect
from deep_translator import GoogleTranslator

def detect_language_and_translate(text: str, target_lang: str = 'en'):
    """
    Detects language and translates to English (if needed).
    Returns both detected language and translated text.
    """
    try:
        lang = detect(text)
    except Exception as e:
        print("Language detection failed:", e)
        lang = 'unknown'

    translated_text = text
    if lang != target_lang and lang != 'unknown':
        try:
            translated_text = GoogleTranslator(source=lang, target=target_lang).translate(text)
        except Exception as e:
            print("Translation failed:", e)

    return lang, translated_text


def translate_back(text: str, target_lang: str):
    """Translate English answer back to user's original language."""
    if target_lang == 'en':
        return text
    try:
        return GoogleTranslator(source='en', target=target_lang).translate(text)
    except Exception as e:
        print("Back translation failed:", e)
        return text
