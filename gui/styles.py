DARK_STYLE = """
QMainWindow {
    background-color: #2b2b2b;
}
QWidget {
    background-color: #2b2b2b;
    color: #ffffff;
}
QPushButton {
    background-color: #3c3c3c;
    border: 1px solid #555;
    padding: 5px;
    border-radius: 4px;
}
QPushButton:hover {
    background-color: #4a4a4a;
}
QPushButton:pressed {
    background-color: #2a2a2a;
}
QListWidget, QTableWidget {
    background-color: #1e1e1e;
    alternate-background-color: #2a2a2a;
    color: #ffffff;
    gridline-color: #444;
}
QHeaderView::section {
    background-color: #3c3c3c;
    color: #ffffff;
    padding: 4px;
}
QSlider::groove:horizontal {
    border: 1px solid #555;
    height: 6px;
    background: #3c3c3c;
    border-radius: 3px;
}
QSlider::handle:horizontal {
    background: #ffffff;
    width: 14px;
    margin: -4px 0;
    border-radius: 7px;
}
QSlider::handle:horizontal:hover {
    background: #cccccc;
}
QCheckBox {
    color: #ffffff;
}
QComboBox {
    background-color: #3c3c3c;
    color: #ffffff;
    border: 1px solid #555;
    padding: 3px;
}
QProgressBar {
    background-color: #3c3c3c;
    color: #ffffff;
    border: 1px solid #555;
    border-radius: 4px;
    text-align: center;
}
QProgressBar::chunk {
    background-color: #66ccff;
    border-radius: 4px;
}
QLabel {
    color: #ffffff;
}
QMenuBar {
    background-color: #2b2b2b;
    color: #ffffff;
}
QMenuBar::item:selected {
    background-color: #3c3c3c;
}
QMenu {
    background-color: #2b2b2b;
    color: #ffffff;
}
QMenu::item:selected {
    background-color: #3c3c3c;
}
"""

LIGHT_STYLE = ""  # можно оставить пустым, тогда используем системную тему