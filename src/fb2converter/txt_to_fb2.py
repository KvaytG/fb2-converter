from .fb2 import FictionBook, get_title_by_file_path
from .internal.encoding_detector import detect_encoding
from .internal.text_cleaner import clean_text


def convert_txt_to_fb2(src_path: str, out_path: str):
    fb2 = FictionBook(get_title_by_file_path(out_path))
    encoding = detect_encoding(src_path, 0, 100_000)
    with open(src_path, 'r', encoding=encoding) as f:
        for line in f:
            line = clean_text(line)
            if line:
                fb2.add_unknown(line)
    fb2.save(out_path)
