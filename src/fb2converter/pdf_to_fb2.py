import re
from io import BytesIO
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTFigure, LTImage
from PIL import Image
from .fb2 import FictionBook, get_title_by_file_path
from .internal.text_cleaner import clean_text

_digits_pattern = re.compile(r'^-?\d+([.,]\d+)?$')


def _extract_elements(pdf_path):
    elements = []
    for page in extract_pages(pdf_path):
        for element in page:
            if isinstance(element, LTTextContainer):
                text = element.get_text()
                text = text.replace('-\n', '').replace('\n', ' ')
                text = clean_text(text)
                if text:
                    elements.append(text)
            elif isinstance(element, LTFigure):
                for item in element:
                    if isinstance(item, LTImage):
                        data = item.stream.get_data()
                        img = Image.open(BytesIO(data))
                        elements.append(img)
    return elements


def convert_pdf_to_fb2(src_path: str, out_path: str, font_path: str):
    fb2 = FictionBook(get_title_by_file_path(out_path))
    for elem in _extract_elements(src_path):
        if isinstance(elem, str):
            if _digits_pattern.match(elem):
                continue
            fb2.add_unknown_text(elem)
        else:
            fb2.add_image(elem)
    fb2.save(out_path, font_path)
