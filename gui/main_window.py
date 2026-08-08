import os
from glob import glob
from pathlib import Path
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from core.worker import CompressionWorker
from core.utils import get_file_size_kb
from gui.styles import DARK_STYLE, LIGHT_STYLE

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔥 Super Compressor")
        self.setMinimumSize(800, 600)

        # Центральный виджет
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Таблица файлов
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Имя файла", "Исходный (КБ)", "Сжатый (КБ)", "Сжатие %"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)

        # Кнопки добавления
        btn_layout = QHBoxLayout()
        btn_add_files = QPushButton("➕ Добавить файлы")
        btn_add_folder = QPushButton("📁 Добавить папку")
        btn_clear = QPushButton("🗑️ Очистить")
        btn_layout.addWidget(btn_add_files)
        btn_layout.addWidget(btn_add_folder)
        btn_layout.addWidget(btn_clear)
        layout.addLayout(btn_layout)

        # === Параметры сжатия ===
        params_layout = QGridLayout()

        # Ручной режим
        self.manual_check = QCheckBox("Ручной режим")
        self.manual_check.setChecked(False)
        params_layout.addWidget(self.manual_check, 0, 0, 1, 2)

        # Ползунок качества
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setRange(1, 100)
        self.quality_slider.setValue(85)
        self.quality_slider.setEnabled(False)
        self.quality_label = QLabel("Качество: 85")
        params_layout.addWidget(self.quality_label, 1, 0)
        params_layout.addWidget(self.quality_slider, 1, 1)

        # Выходной формат
        self.format_combo = QComboBox()
        self.format_combo.addItems(["Исходный", "PNG", "JPEG", "WebP"])
        params_layout.addWidget(QLabel("Выходной формат:"), 2, 0)
        params_layout.addWidget(self.format_combo, 2, 1)

        # Нумерация
        self.rename_check = QCheckBox("Нумеровать файлы (1, 2, 3...)")
        params_layout.addWidget(self.rename_check, 3, 0, 1, 2)

        # === НОВОЕ: Общая папка сохранения ===
        self.save_folder_check = QCheckBox("Сохранять в общую папку")
        self.save_folder_check.setChecked(False)
        params_layout.addWidget(self.save_folder_check, 4, 0, 1, 1)

        # Поле с путём и кнопки
        self.save_folder_edit = QLineEdit()
        self.save_folder_edit.setReadOnly(True)
        self.save_folder_edit.setPlaceholderText("Путь к папке сохранения")
        self.save_folder_edit.setEnabled(False)
        params_layout.addWidget(self.save_folder_edit, 4, 1, 1, 2)

        # Кнопка "Обзор" и "Открыть папку"
        folder_btn_layout = QHBoxLayout()
        self.save_folder_browse = QPushButton("Обзор...")
        self.save_folder_browse.setEnabled(False)
        self.save_folder_open = QPushButton("📂 Открыть папку")
        self.save_folder_open.setEnabled(False)
        folder_btn_layout.addWidget(self.save_folder_browse)
        folder_btn_layout.addWidget(self.save_folder_open)
        params_layout.addLayout(folder_btn_layout, 5, 0, 1, 3)

        # Темная тема
        self.dark_theme_check = QCheckBox("Тёмная тема")
        self.dark_theme_check.setChecked(True)
        params_layout.addWidget(self.dark_theme_check, 6, 0, 1, 2)

        # Кнопка помощи
        self.help_button = QPushButton("❓ Помощь")
        params_layout.addWidget(self.help_button, 6, 2, 1, 1)

        layout.addLayout(params_layout)

        # Кнопка сжатия и прогресс
        self.btn_compress = QPushButton("🚀 Сжать!")
        self.btn_compress.clicked.connect(self.start_compression)
        layout.addWidget(self.btn_compress)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        layout.addWidget(self.progress)

                # ----- Социальные кнопки -----
        social_layout = QHBoxLayout()
        social_layout.addStretch()

        social_links = {
            "▶️ YouTube": "https://www.youtube.com/@derivangos",
            "✈️ Telegram": "https://t.me/bitcoinblyat",
            "📘 VK": "https://vk.ru/d6ctor",
            "📸 Instagram": "https://www.instagram.com/d6ct6r/"
        }

        for text, url in social_links.items():
            btn = QPushButton(text)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: none;
                    color: #66ccff;
                    font-weight: bold;
                    text-decoration: underline;
                    padding: 4px 8px;
                }
                QPushButton:hover {
                    color: #99ddff;
                }
            """)
            btn.clicked.connect(lambda checked, u=url: self.open_link(u))
            social_layout.addWidget(btn)

        social_layout.addStretch()
        layout.addLayout(social_layout)
        
        # --- Соединения сигналов ---
        btn_add_files.clicked.connect(self.add_files)
        btn_add_folder.clicked.connect(self.add_folder)
        btn_clear.clicked.connect(self.clear_all)
        self.manual_check.toggled.connect(self.on_manual_toggled)
        self.quality_slider.valueChanged.connect(self.on_quality_changed)
        self.dark_theme_check.toggled.connect(self.on_theme_toggled)
        self.format_combo.currentTextChanged.connect(self.on_format_changed)

        # Новые сигналы
        self.save_folder_check.toggled.connect(self.on_save_folder_toggled)
        self.save_folder_browse.clicked.connect(self.on_browse_folder)
        self.save_folder_open.clicked.connect(self.on_open_folder)
        self.help_button.clicked.connect(self.show_help)

        # --- Инициализация данных ---
        self.files = []
        self.worker = None

        # Устанавливаем путь по умолчанию для общей папки
        default_path = os.path.expanduser("~/Pictures/Compressed")
        if not os.path.exists(default_path):
            try:
                os.makedirs(default_path)
            except:
                pass
        self.save_folder_edit.setText(default_path)

        # Применяем тему
        self.setStyleSheet(DARK_STYLE)

    # ------ Добавление файлов (без изменений) ------
    def add_files(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Выберите изображения", "",
            "Images (*.png *.jpg *.jpeg *.webp *.bmp *.tiff)"
        )
        for p in paths:
            if p not in self.files:
                self.files.append(p)
                self._add_table_row(p)

    def add_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if folder:
            exts = ('*.png', '*.jpg', '*.jpeg', '*.webp', '*.bmp', '*.tiff')
            for ext in exts:
                for f in glob(os.path.join(folder, ext)):
                    if f not in self.files:
                        self.files.append(f)
                        self._add_table_row(f)

    def clear_all(self):
        self.files.clear()
        self.table.setRowCount(0)

    def _add_table_row(self, filepath):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(os.path.basename(filepath)))
        size_kb = get_file_size_kb(filepath)
        self.table.setItem(row, 1, QTableWidgetItem(f"{size_kb:.2f}"))
        self.table.setItem(row, 2, QTableWidgetItem("—"))
        self.table.setItem(row, 3, QTableWidgetItem("—"))

    # ------ Обработчики параметров ------
    def on_manual_toggled(self, checked):
        self.quality_slider.setEnabled(checked)
        if not checked:
            fmt = self.format_combo.currentText()
            default_q = 85 if fmt == "JPEG" else 80
            self.quality_slider.setValue(default_q)
            self.quality_label.setText(f"Качество: {default_q}")

    def on_quality_changed(self, value):
        self.quality_label.setText(f"Качество: {value}")

    def on_format_changed(self, fmt):
        if not self.manual_check.isChecked():
            default_q = 85 if fmt == "JPEG" else 80
            self.quality_slider.setValue(default_q)
            self.quality_label.setText(f"Качество: {default_q}")

    # ------ НОВОЕ: работа с папкой сохранения ------
    def on_save_folder_toggled(self, checked):
        self.save_folder_edit.setEnabled(checked)
        self.save_folder_browse.setEnabled(checked)
        self.save_folder_open.setEnabled(checked)
        if checked and not self.save_folder_edit.text():
            # если путь пуст, ставим дефолтный
            default_path = os.path.expanduser("~/Pictures/Compressed")
            self.save_folder_edit.setText(default_path)

    def on_browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения сжатых файлов")
        if folder:
            self.save_folder_edit.setText(folder)

    def on_open_folder(self):
        folder = self.save_folder_edit.text()
        if folder and os.path.exists(folder):
            QDesktopServices.openUrl(QUrl.fromLocalFile(folder))
        else:
            QMessageBox.warning(self, "Ошибка", "Папка не существует!")

    # ------ Помощь ------
    def show_help(self):
        help_text = (
            "🔥 Super Compressor – простой и быстрый!\n\n"
            "1. Добавьте файлы или папку с картинками.\n"
            "2. Настройте сжатие:\n"
            "   • Ручной режим – крутите ползунок качества.\n"
            "   • Выходной формат – все картинки будут конвертированы в выбранный.\n"
            "   • Нумерация – переименует файлы в 1.png, 2.png …\n"
            "   • Сохранять в общую папку – выберите одну папку для всех сжатых файлов.\n"
            "3. Нажмите «Сжать!» и ждите.\n"
            "4. Результаты появятся в таблице, а файлы – в папке (compressed рядом с оригиналом или в выбранной общей).\n\n"
            "Приятного использования! 🚀"
        )
        QMessageBox.information(self, "Помощь", help_text)

    # ------ Тёмная тема ------
    def on_theme_toggled(self, checked):
        self.setStyleSheet(DARK_STYLE if checked else LIGHT_STYLE)
        
    def open_link(self, url):
        """Открывает ссылку в браузере"""
        from PySide6.QtGui import QDesktopServices
        from PySide6.QtCore import QUrl
        QDesktopServices.openUrl(QUrl(url))

    # ------ Запуск сжатия ------
    def start_compression(self):
        if not self.files:
            QMessageBox.warning(self, "Нет файлов", "Добавьте изображения!")
            return

        quality = self.quality_slider.value()
        manual = self.manual_check.isChecked()
        out_format = self.format_combo.currentText()
        rename = self.rename_check.isChecked()

        # Определяем папку сохранения
        save_folder = None
        if self.save_folder_check.isChecked():
            save_folder = self.save_folder_edit.text().strip()
            if not save_folder:
                QMessageBox.warning(self, "Ошибка", "Укажите папку для сохранения!")
                return
            if not os.path.exists(save_folder):
                try:
                    os.makedirs(save_folder)
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не могу создать папку:\n{e}")
                    return

        self.worker = CompressionWorker(
            self.files, quality, manual, out_format, rename, save_folder
        )
        self.worker.progress_signal.connect(self.progress.setValue)
        self.worker.file_done_signal.connect(self.on_file_done)
        self.worker.finished_signal.connect(self.on_compression_finished)
        self.worker.error_signal.connect(lambda msg: QMessageBox.critical(self, "Ошибка", msg))
        self.worker.start()

        self.btn_compress.setEnabled(False)
        self.progress.setValue(0)

    def on_file_done(self, output_path, original_size, compressed_size):
        base_name = os.path.basename(output_path)
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item and item.text() == base_name:
                self.table.setItem(row, 2, QTableWidgetItem(f"{compressed_size:.2f}"))
                if original_size > 0:
                    ratio = (1 - compressed_size / original_size) * 100
                    self.table.setItem(row, 3, QTableWidgetItem(f"{ratio:.1f}%"))
                break

    def on_compression_finished(self):
        self.btn_compress.setEnabled(True)
        QMessageBox.information(self, "Готово", "Сжатие завершено!")
        self.progress.setValue(100)

    def closeEvent(self, event):
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
        event.accept()