import re

_non_breaking_spaces_pattern = re.compile(r'[\u202f\u00a0]')
_zero_width_chars_pattern = re.compile(r'[\u200b-\u200d\uFEFF]')
_space_pattern = re.compile(r'\s+')


def clean_text(text: str) -> str:
    """ INTERNAL FUNCTION! """
    text = _non_breaking_spaces_pattern.sub(' ', text)
    text = _zero_width_chars_pattern.sub('', text)
    text = _space_pattern.sub(' ', text)
    return text.strip()
