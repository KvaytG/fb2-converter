import os
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from PIL import Image
from bs4 import BeautifulSoup
from .fb2 import FictionBook


def convert_epub_to_fb2(src_path: str, out_path: str, font_path: str):
    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(src_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)
        container_path = os.path.join(tmpdir, 'META-INF', 'container.xml')
        if not os.path.exists(container_path):
            raise FileNotFoundError("EPUB structure invalid: META-INF/container.xml missing")
        container_tree = ET.parse(container_path)
        container_root = container_tree.getroot()
        ns = {'ns': 'urn:oasis:names:tc:opendocument:xmlns:container'}
        rootfile = container_root.find('.//ns:rootfile', ns)
        opf_path = rootfile.get('full-path')
        opf_full_path = os.path.join(tmpdir, opf_path)
        opf_tree = ET.parse(opf_full_path)
        opf_root = opf_tree.getroot()
        opf_ns = {
            'opf': 'http://www.idpf.org/2007/opf',
            'dc': 'http://purl.org/dc/elements/1.1/'
        }
        title = opf_root.find('.//dc:title', opf_ns).text
        fb2 = FictionBook(title)
        manifest = {}
        manifest_elem = opf_root.find('.//opf:manifest', opf_ns)
        for item in manifest_elem.findall('opf:item', opf_ns):
            item_id = item.get('id')
            item_href = item.get('href')
            item_media_type = item.get('media-type')
            manifest[item_id] = (item_href, item_media_type)
        spine = []
        spine_elem = opf_root.find('.//opf:spine', opf_ns)
        for itemref in spine_elem.findall('opf:itemref', opf_ns):
            spine.append(itemref.get('idref'))
        opf_dir = os.path.dirname(opf_full_path)
        for item_id in spine:
            if item_id not in manifest:
                continue
            item_href, media_type = manifest[item_id]
            if media_type not in ['application/xhtml+xml', 'text/html']:
                continue
            html_path = os.path.normpath(os.path.join(opf_dir, item_href))
            if not os.path.exists(html_path):
                continue
            with open(html_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
            process_html_content(soup, fb2, os.path.dirname(html_path))
        fb2.save(out_path, font_path)


def process_html_content(soup, fb2, base_dir):
    def traverse(element):
        if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            text = element.get_text(strip=True)
            if text:
                fb2.add_title(text)
        elif element.name == 'p':
            text = element.get_text(strip=True)
            if text:
                fb2.add_text(text)
        elif element.name == 'img':
            src = element.get('src', '')
            if src:
                img_path = os.path.normpath(os.path.join(base_dir, src))
                if os.path.exists(img_path):
                    try:
                        img = Image.open(img_path)
                        ext = os.path.splitext(img_path)[1].lower()
                        content_type = 'image/png' if ext == '.png' else 'image/jpeg'
                        fb2.add_image(img, contentType=content_type)
                    except Exception as e:
                        print(f"Skipped image {img_path}: {str(e)}")
        if hasattr(element, 'children'):
            for child in element.children:
                if child.name:
                    traverse(child)
    body = soup.find('body') or soup
    if body:
        traverse(body)
