import uuid
import xml.etree.ElementTree as ET
from datetime import datetime
from .internal.text_cleaner import clean_text
from .internal.title_matcher import is_title


def _create_fb2_template(title: str):
    ns = {
        'xmlns': 'http://www.gribuser.ru/xml/fictionbook/2.0',
        'xmlns:l': 'http://www.w3.org/1999/xlink'
    }
    root = ET.Element('FictionBook', attrib=ns)
    description = ET.SubElement(root, 'description')

    title_info = ET.SubElement(description, 'title-info')
    ET.SubElement(title_info, 'genre').text = 'unknown'
    author = ET.SubElement(title_info, 'author')
    ET.SubElement(author, 'first-name').text = 'Unknown'
    ET.SubElement(author, 'last-name').text = 'Author'
    ET.SubElement(title_info, 'book-title').text = title
    ET.SubElement(title_info, 'lang').text = 'mul'

    doc_info = ET.SubElement(description, 'document-info')
    doc_author = ET.SubElement(doc_info, 'author')
    ET.SubElement(doc_author, 'nickname').text = 'KvaytG'
    ET.SubElement(doc_info, 'program-used').text = 'https://github.com/KvaytG/fb2-converter'

    current_date = datetime.now()
    doc_date = ET.SubElement(doc_info, 'date', value=current_date.strftime('%Y-%m-%d'))
    doc_date.text = current_date.strftime('%Y')

    ET.SubElement(doc_info, 'id').text = str(uuid.uuid4())
    ET.SubElement(doc_info, 'version').text = '1.0.0'

    body = ET.SubElement(root, 'body')
    title_section = ET.SubElement(body, 'title')
    ET.SubElement(title_section, 'p').text = title

    return root, body


class FictionBook:
    def __init__(self, title: str):
        self._root, self._body = _create_fb2_template(title)
        self._current_section = None
        self._last_title_element = None
        self._headings = []

    def add_title(self, title: str, check: bool = True):
        title = clean_text(title)
        if check and not title:
            return
        if self._last_title_element and not self._section_has_text():
            ET.SubElement(self._last_title_element, 'p').text = title
        else:
            section = ET.SubElement(self._body, 'section')
            number = len(self._headings) + 1
            section_id = f'section_{number}'
            section.set('id', section_id)
            self._headings.append((section_id, f'{number}. {title}'))
            title_element = ET.SubElement(section, 'title')
            ET.SubElement(title_element, 'p').text = title
            self._current_section = section
            self._last_title_element = title_element

    def add_text(self, text: str, check: bool = True):
        text = clean_text(text)
        if check and not text:
            return
        self._last_title_element = None
        parent = self._current_section or self._body
        ET.SubElement(parent, 'p').text = text

    def _section_has_text(self) -> bool:
        if self._current_section is None:
            return False
        for elem in self._current_section:
            if elem.tag == 'p':
                return True
        return False

    def add_unknown(self, text: str):
        text = clean_text(text)
        if text:
            self.add_title(text, False) if is_title(text) else self.add_text(text, False)

    def save(self, path: str):
        if self._headings:
            toc_section = ET.Element('section')
            toc_title = ET.SubElement(toc_section, 'title')
            ET.SubElement(toc_title, 'p').text = 'Содержание'
            for section_id, title_text in self._headings:
                p = ET.SubElement(toc_section, 'p')
                a = ET.SubElement(p, 'a', attrib={'l:href': f'#{section_id}'})
                a.text = title_text
            body_children = list(self._body)
            for child in body_children:
                self._body.remove(child)
            self._body.append(body_children[0])
            self._body.append(toc_section)
            for child in body_children[1:]:
                self._body.append(child)
        tree = ET.ElementTree(self._root)
        if hasattr(ET, 'indent'):
            ET.indent(tree, space='\t', level=0)
        tree.write(
            path,
            encoding='utf-8',
            xml_declaration=True,
            short_empty_elements=False
        )


def get_title_by_file_path(file_path: str):
    return file_path[:-4] if file_path.endswith('.fb2') else file_path
