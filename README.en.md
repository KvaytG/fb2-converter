
# fb2-converter

![Python 3.10](https://img.shields.io/badge/Python-3.10-blue?logo=python) ![MIT License](https://img.shields.io/badge/License-MIT-green) [![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-red)](https://kvaytg.ru/donate.php?lang=en)

Simple converter from TXT, PDF and EPUB to FB2 format.

## 📚 Usage

```python
from fb2_converter import convert_txt_to_fb2,\
    convert_pdf_to_fb2, convert_epub_to_fb2

# Convert TXT to FB2
convert_txt_to_fb2('input.txt', 'output.fb2', 'example-font.ttf')

# Convert PDF to FB2
convert_pdf_to_fb2('input.pdf', 'output.fb2', 'example-font.ttf')

# Convert EPUB to FB2
convert_epub_to_fb2('input.epub', 'output.fb2', 'example-font.ttf')
```

## ⚙️ Installation
```bash
pip install git+https://github.com/KvaytG/fb2-converter.git
```

## 📜 License
Licensed under the **[MIT](LICENSE.txt)** license.

This project uses open-source components. For license details see **[pyproject.toml](pyproject.toml)** and dependencies' official websites.
