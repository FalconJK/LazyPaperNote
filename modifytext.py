import re

from googletrans import Translator
translator = Translator(service_urls=[
    'translate.google.com.tw',
    'translate.google.com',
])

def modify_en_text(text, modify_mode='BASIC', keep_emoji=True):
    """ Make your text easy to read and to translate.

        Args:
            text(str):
                target dirty text.
            modify_mode(str):
                mode selection
            keep_emoji(bool):
                call back remove_emoji func or not.

        Returns:
            text_output(str):
                formatted output.

    """
    if not keep_emoji:
        text = remove_emoji(text)

    sents = split_text_to_sentences_en(text)
    text_output = mode_factory(modify_mode)(sents)

    return text_output


def remove_emoji(text):
    """ Remove emoji. """
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)

    return emoji_pattern.sub(r'', text)


def split_text_to_sentences_en(text):
    """ Make your text easy to read and to translate.

        Args:
            text(str):
                target dirty text.
        Returns:
            sents(list):
                sentences splited.

    """

    text = text.replace(" . . . ", "...")  # replace LaTex ellipses with original ellipses

    sents = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)

    return sents


def mode_factory(modify_mode):
    if modify_mode == "BASIC":
        return mode_basic

    if modify_mode == 'LIST-MARK':
        return mode_listmark

    if modify_mode == 'MarkDown':
        return mode_markdown


def mode_basic(sents):
    clear_text = [' '.join(_s.split()) for _s in sents]
    text_output = '\n\n'.join(clear_text)
    return text_output


def mode_listmark(sents):
    clear_text = [' '.join(_s.split()) for _s in sents]
    listmaker = ['- '+ _s for _s in clear_text]
    text_output = '\n\n'.join(listmaker)

    return text_output


def mode_markdown(sents):
    clear_text = [' '.join(_s.split()) for _s in sents]
    translations = translator.translate(clear_text, dest='zh-TW')
    to_markdown = ['*' + s.origin + '*\n>' + s.text for s in translations]

    text_output = '\n\n'.join(to_markdown)
    return text_output
