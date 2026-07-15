
# fb2-converter

![US](https://kvaytg.ru/common/flags/us-21x16.svg) **English** | [![RU](https://kvaytg.ru/common/flags/ru-21x16.svg) Русский](README.ru.md)

![Python 3.10](https://img.shields.io/badge/Python-3.10-blue?logo=python) ![PolyForm License](https://img.shields.io/badge/License-PolyForm-blue) [![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-red)](https://kvaytg.ru/donate.php?lang=en)

Simple converter from TXT, PDF and EPUB to FB2 format.

## 📚 Usage
```python
from fb2_converter import convert_txt_to_fb2, \
    convert_pdf_to_fb2, convert_epub_to_fb2

# Convert TXT to FB2
convert_txt_to_fb2('input.txt', 'output.fb2', 'example-font.ttf')

# Convert PDF to FB2
convert_pdf_to_fb2('input.pdf', 'output.fb2', 'example-font.ttf')

# Convert EPUB to FB2
convert_epub_to_fb2('input.epub', 'output.fb2', 'example-font.ttf')
```

## 📥 Installation
```bash
pip install git+https://github.com/KvaytG/fb2-converter.git
```

## 📝 License
Licensed under the **[PolyForm Noncommercial](LICENSE.md)** license.

This project uses open-source components. For license details see **[pyproject.toml](pyproject.toml)** and dependencies' official websites.
