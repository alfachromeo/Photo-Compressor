from PySide6.QtCore import QThread, Signal
from core.compressor import compress_image
from core.utils import get_file_size_kb
from pathlib import Path
import os

class CompressionWorker(QThread):
    progress_signal = Signal(int)
    file_done_signal = Signal(str, float, float)  # путь к сжатому файлу, исходный размер, сжатый
    finished_signal = Signal()
    error_signal = Signal(str)

    def __init__(self, files, quality, manual, out_format, rename, save_folder=None):
        super().__init__()
        self.files = files
        self.quality = quality
        self.manual = manual
        self.out_format = out_format
        self.rename = rename
        self.save_folder = save_folder  # может быть None

    def run(self):
        try:
            total = len(self.files)
            for i, filepath in enumerate(self.files):
                input_ext = Path(filepath).suffix.lower()
                if self.out_format == "Исходный":
                    out_ext = input_ext
                    out_format_name = input_ext[1:].upper()
                else:
                    out_ext = f".{self.out_format.lower()}"
                    out_format_name = self.out_format

                # Качество
                if self.manual:
                    quality = self.quality
                else:
                    if out_format_name == 'JPEG':
                        quality = 85
                    elif out_format_name in ('PNG', 'WEBP'):
                        quality = 80
                    else:
                        quality = 85

                base = Path(filepath).stem

                # ---- Определяем выходную папку и имя ----
                if self.save_folder:
                    # Общая папка
                    out_dir = Path(self.save_folder)
                else:
                    # Рядом с оригиналом в папке compressed
                    out_dir = Path(filepath).parent / "compressed"
                out_dir.mkdir(parents=True, exist_ok=True)

                # Имя файла
                if self.rename:
                    name = f"{i+1}{out_ext}"
                else:
                    name = f"{base}_compressed{out_ext}"

                # Проверяем конфликт имён
                output_path = out_dir / name
                counter = 1
                while output_path.exists():
                    stem = output_path.stem
                    # если в имени уже есть суффикс _1, увеличиваем
                    if stem.endswith(f"_{counter-1}"):
                        stem = stem[:-len(f"_{counter-1}")]
                    output_path = out_dir / f"{stem}_{counter}{out_ext}"
                    counter += 1

                # Сжатие
                original_size = get_file_size_kb(filepath)
                compress_image(filepath, output_path, out_format_name, quality)
                compressed_size = get_file_size_kb(output_path)

                self.file_done_signal.emit(str(output_path), original_size, compressed_size)
                self.progress_signal.emit(int((i+1)/total*100))

            self.finished_signal.emit()
        except Exception as e:
            self.error_signal.emit(str(e))