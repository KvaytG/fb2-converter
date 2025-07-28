import io
import base64
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime
from PIL import Image
from captionforge import generate_caption_image
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
        self._title = title
        self._root, self._body = _create_fb2_template(title)
        self._current_section = None
        self._last_title_element = None
        self._headings = []
        self._start_new_section(has_title=False)

    def _start_new_section(self, has_title: bool = True):
        self._current_section = ET.SubElement(self._body, 'section')
        self._last_title_element = None
        if has_title:
            number = len(self._headings) + 1
            section_id = f'section_{number}'
            self._current_section.set('id', section_id)
            return section_id
        return None

    def _section_has_text(self) -> bool:
        if self._current_section is None:
            return False
        for elem in self._current_section:
            if elem.tag == 'p':
                return True
        return False

    def add_title(self, title: str, check: bool = True):
        title = clean_text(title)
        if check and not title:
            return
        if self._last_title_element and not self._section_has_text():
            ET.SubElement(self._last_title_element, 'p').text = title
        else:
            section_id = self._start_new_section(has_title=True)
            self._headings.append((section_id, f'{len(self._headings) + 1}. {title}'))
            title_element = ET.SubElement(self._current_section, 'title')
            ET.SubElement(title_element, 'p').text = title
            self._last_title_element = title_element

    def add_text(self, text: str, check: bool = True):
        text = clean_text(text)
        if check and not text:
            return
        self._last_title_element = None
        ET.SubElement(self._current_section, 'p').text = text

    def add_unknown_text(self, text: str):
        text = clean_text(text)
        if not text:
            return
        if is_title(text):
            self.add_title(text, False)
        else:
            self.add_text(text, False)

    def add_image(self, image: Image.Image, imageId: str = None, contentType: str = 'image/jpeg') -> str:
        if imageId is None:
            imageId = f'image_{uuid.uuid4().hex[:8]}.jpg'

        buffer = io.BytesIO()
        image.save(buffer, format=contentType.split('/')[-1].upper())
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        binary_elem = ET.Element('binary', id=imageId, content_type=contentType)
        binary_elem.text = img_base64

        body_index = list(self._root).index(self._body)
        self._root.insert(body_index, binary_elem)

        image_elem = ET.Element('image', attrib={'l:href': f'#{imageId}'})
        self._current_section.append(image_elem)

        return imageId

    def save(self, path: str, font_path: str):
        img = generate_caption_image(
            pil_image=Image.new('RGB', (400, 564), (255, 255, 255)),
            text=self._title,
            text_color=(0, 0, 0),
            font_path=font_path
        )
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

        binary_elem = ET.Element('binary', id='cover.jpg', content_type='image/jpeg')
        binary_elem.text = img_base64
        body_index = list(self._root).index(self._body)
        self._root.insert(body_index, binary_elem)

        description = self._root.find('description')
        title_info = description.find('title-info')

        coverpage = ET.Element('coverpage')
        image_elem = ET.Element(f'image')
        image_elem.set('l:href', '#cover.jpg')
        coverpage.append(image_elem)

        book_title = title_info.find('book-title')
        index = list(title_info).index(book_title) + 1
        title_info.insert(index, coverpage)

        if self._headings:
            toc_section = ET.Element('section')
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
