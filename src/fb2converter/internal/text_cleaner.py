import re

non_breaking_spaces_pattern = re.compile(r'[\u202f\u00a0]')
zero_width_chars_pattern = re.compile(r'[\u200b-\u200d\uFEFF]')
space_pattern = re.compile(r'\s+')


def clean_text(text: str) -> str:
    """ INTERNAL FUNCTION! """
    text = non_breaking_spaces_pattern.sub(' ', text)
    text = zero_width_chars_pattern.sub('', text)
    text = space_pattern.sub(' ', text)
    return text.strip()
