import os

def get_file_size_kb(path):
    """Возвращает размер файла в килобайтах (округлённо)"""
    size = os.path.getsize(path)
    return round(size / 1024, 2)