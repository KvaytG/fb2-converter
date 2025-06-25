import re
import os
import logging
from .text_cleaner import clean_text

logging.basicConfig(level=logging.ERROR)
_logger = logging.getLogger(__name__)

_edge_symbols_pattern = re.compile(r'^[★*\[\s=]+|[★*\]\s=]+$')


def _load_title_patterns(file_path: str) -> list[re.Pattern]:
    patterns = []
    try:
        dir_path = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(dir_path, file_path)
        with open(full_path, 'r', encoding='utf-8') as f:
            for num, line in enumerate(f, start=1):
                line = clean_text(line)
                if not line or line.startswith('#'):
                    continue
                try:
                    patterns.append(re.compile(line))
                except re.error:
                    _logger.error(f"Invalid regex at line {num}: {line}")
    except FileNotFoundError:
        _logger.error(f"Pattern file not found: {file_path}")
    return patterns


_patterns = _load_title_patterns("../../../data/title-patterns.txt")


def _is_all_caps(text: str) -> bool:
    return any(c.isalpha() for c in text) and not any(c.islower() for c in text)


def is_title(text: str) -> bool:
    """ INTERNAL FUNCTION! """
    text = clean_text(text)
    if not text:
        return False
    text = _edge_symbols_pattern.sub('', text)
    if len(text) > 50 or text.startswith(('—', '–')) or text.endswith(('.', '!', '?')):
        return False
    if _is_all_caps(text):
        return True
    return any(p.match(text) for p in _patterns)
