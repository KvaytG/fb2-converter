
# fb2-converter

[![US](https://kvaytg.ru/common/flags/us-21x16.svg) English](README.md) | ![RU](https://kvaytg.ru/common/flags/ru-21x16.svg) **Русский**

![Python 3.10](https://img.shields.io/badge/Python-3.10-blue?logo=python) ![PolyForm License](https://img.shields.io/badge/License-PolyForm-blue) [![Sponsor](https://img.shields.io/badge/Поддержать-%E2%9D%A4-red)](https://kvaytg.ru/donate.php?lang=ru)

Простой конвертер из форматов TXT, PDF и EPUB в FB2.

## 📚 Использование
```python
from fb2_converter import convert_txt_to_fb2, \
    convert_pdf_to_fb2, convert_epub_to_fb2

# Конвертация TXT в FB2
convert_txt_to_fb2('input.txt', 'output.fb2', 'example-font.ttf')

# Конвертация PDF в FB2
convert_pdf_to_fb2('input.pdf', 'output.fb2', 'example-font.ttf')

# Конвертация EPUB в FB2
convert_epub_to_fb2('input.epub', 'output.fb2', 'example-font.ttf')
```

## 📥 Установка
```bash
pip install git+https://github.com/KvaytG/fb2-converter.git
```

## 📝 Лицензия
Распространяется по лицензии **[PolyForm Noncommercial](LICENSE.md)**.

Проект использует компоненты с открытым исходным кодом. Сведения о лицензиях см. в **[pyproject.toml](pyproject.toml)** и на официальных ресурсах зависимостей.
