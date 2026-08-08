# 🔥 Super Compressor

> Максимальное сжатие изображений с сохранением качества – просто, быстро, удобно.

[https://img.shields.io/badge/Python-3.12-blue](https://img.shields.io/badge/Python-3.12-blue) [https://img.shields.io/badge/PySide6-6.11.1-brightgreen](https://img.shields.io/badge/PySide6-6.11.1-brightgreen) [https://img.shields.io/badge/License-MIT-green](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Описание

**Super Compressor** – это десктопное приложение для пакетного сжатия изображений.  
Оно работает с популярными форматами (PNG, JPEG, WebP, BMP, TIFF) и позволяет:

- Сжимать файлы без потери визуального качества.
    
- Конвертировать все изображения в один формат.
    
- Управлять степенью сжатия вручную или автоматически.
    
- Сохранять результаты в общую папку или рядом с оригиналами.
    
- Переименовывать файлы с нумерацией.
    

Интерфейс выполнен в тёмной теме, интуитивно понятен и не требует специальных знаний.

---

## 🎯 Возможности

- **Загрузка файлов и папок** – добавьте любое количество изображений.
    
- **Ручной и автоматический режим** – ползунок качества или авто-подбор.
    
- **Выбор выходного формата** – PNG, JPEG, WebP или исходный.
    
- **Нумерация файлов** – включите галочку, и файлы будут переименованы в `1.png`, `2.png` …
    
- **Общая папка сохранения** – все сжатые файлы складываются в одну выбранную папку.
    
- **Таблица с результатами** – видите исходный размер, сжатый и процент сжатия.
    
- **Тёмная тема** – по умолчанию, легко отключается.
    
- **Встроенная справка** – краткая инструкция внутри приложения.
    
- **Кроссплатформенность** – работает на Windows, Linux, macOS (сборка под каждую ОС).
    

---

## 📸 Скриншоты

_Вставьте сюда скриншоты вашего приложения_

---

## 🚀 Установка и запуск

### Для пользователей (готовый EXE)

Скачайте последнюю версию `SuperCompressor.exe` из раздела [Releases](https://github.com/%D0%B2%D0%B0%D1%88-%D0%B0%D0%BA%D0%BA%D0%B0%D1%83%D0%BD%D1%82/super-compressor/releases).  
Просто запустите файл – никаких дополнительных установок не требуется.

---

### Для разработчиков (запуск из исходников)

1. **Клонируйте репозиторий:**
    
    bash
    
    git clone https://github.com/ваш-аккаунт/super-compressor.git
    cd super-compressor
    
2. **Создайте виртуальное окружение (Python 3.12):**
    
    bash
    
    python -m venv .venv
    source .venv/bin/activate      # Linux/macOS
    .venv\Scripts\activate         # Windows
    
3. **Установите зависимости:**
    
    bash
    
    pip install -r requirements.txt
    
4. **Запустите приложение:**
    
    bash
    
    python main.py
    

---

## 🛠️ Сборка собственного EXE

Если вы хотите собрать приложение самостоятельно:

bash

pip install pyinstaller
pyinstaller --onefile --windowed --name="SuperCompressor" --icon=icon.ico main.py

Готовый файл появится в папке `dist/`.

---

## 📂 Структура проекта

text

super-compressor/
├── core/                # Логика сжатия и фоновые задачи
│   ├── compressor.py
│   ├── utils.py
│   └── worker.py
├── gui/                 # Графический интерфейс
│   ├── main_window.py
│   └── styles.py
├── main.py              # Точка входа
├── requirements.txt     # Зависимости
├── README.md            # Этот файл
└── LICENSE              # Лицензия MIT

---

## 🧑‍💻 Контакты и соцсети

Если у вас есть вопросы, предложения или вы хотите поддержать проект – подписывайтесь:

[](https://www.youtube.com/@derivangos)[https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)  
[](https://t.me/bitcoinblyat)[https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)  
[](https://vk.ru/d6ctor)[https://img.shields.io/badge/VK-4680C2?style=for-the-badge&logo=vk&logoColor=white](https://img.shields.io/badge/VK-4680C2?style=for-the-badge&logo=vk&logoColor=white)  
[](https://www.instagram.com/d6ct6r/)[https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)

---

## 📜 Лицензия

Проект распространяется под лицензией MIT – вы можете свободно использовать, модифицировать и распространять код.

---

**Сделано с ❤️ для вас**