# fb2-converter

Simple converter from TXT and PDF to FictionBook 2.0 (FB2) format

## 📚 Usage
```python
from fb2converter import convert_txt_to_fb2, convert_pdf_to_fb2

# Convert text file
convert_txt_to_fb2("input.txt", "output.fb2")

# Convert PDF file
convert_pdf_to_fb2("input.pdf", "output.fb2")
```

## ⚙️ Installation
1. Clone the repository
```bash
git clone https://github.com/KvaytG/fb2-converter.git
cd fb2-converter
```
2. Create a virtual environment and install dependencies
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -e .
```

## 📜 License
fb2-converter is licensed under the **[MIT license](https://opensource.org/license/mit)**.
