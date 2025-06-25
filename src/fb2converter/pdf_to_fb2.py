import re
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
from .fb2 import FictionBook, get_title_by_file_path
from .internal.text_cleaner import clean_text

_digits_pattern = re.compile(r'^-?\d+([.,]\d+)?$')


def _extract_paragraphs(pdf_path):
    texts = []
    for page in extract_pages(pdf_path):
        for element in page:
            if isinstance(element, LTTextContainer):
                text = element.get_text()
                text = text.replace('-\n', '').replace('\n', ' ')
                text = clean_text(text)
                if text:
                    texts.append(text)
    return texts


def convert_pdf_to_fb2(src_path: str, out_path: str, remove_digits: bool = True):
    fb2 = FictionBook(get_title_by_file_path(out_path))
    for paragraph in _extract_paragraphs(src_path):
        if remove_digits and _digits_pattern.match(paragraph):
            continue
        fb2.add_unknown(paragraph)
    fb2.save(out_path)
