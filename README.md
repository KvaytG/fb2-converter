# fb2-converter

Simple converter from TXT and PDF to FictionBook 2.0 (FB2) format

## 📚 Usage
```python
from fb2converter import convert_txt_to_fb2, convert_pdf_to_fb2

# Convert TXT to FB2
convert_txt_to_fb2('input.txt', 'output.fb2', 'example-font.ttf')

# Convert PDF to FB2
convert_pdf_to_fb2('input.pdf', 'output.fb2', 'example-font.ttf')
```

## ⚙️ Installation
```bash
pip install git+https://github.com/KvaytG/fb2-converter.git
```

## 📜 License
fb2-converter is licensed under the **[MIT license](https://opensource.org/license/mit)**.

This project uses open-source components. For license details see **[pyproject.toml](pyproject.toml)** and dependencies' official websites.
