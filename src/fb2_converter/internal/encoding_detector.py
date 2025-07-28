from chardet import UniversalDetector

_detector = UniversalDetector()


def detect_encoding(file_path: str, start_position: int, chunk_size: int) -> str:
    """ INTERNAL FUNCTION! """
    with open(file_path, 'rb') as file:
        file.seek(start_position)
        chunk = file.read(chunk_size)
        _detector.feed(chunk)
        _detector.close()
    return _detector.result['encoding']
