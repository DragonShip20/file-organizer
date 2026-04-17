from PyQt6.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton, QGridLayout, QSizePolicy, QFrame, QFileDialog, QLabel, QGraphicsDropShadowEffect)
from PyQt6.QtCore import (Qt)
from PyQt6.QtGui import (QFont, QColor)
import os, shutil, sys

GROUPS = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tif", ".tiff"},
    "Documents": {".pdf", ".docx", ".doc", ".txt", ".odt", ".rtf"},
    "Archives": {".zip", ".tar", ".gz", ".tgz", ".rar", ".7z"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".m4a"},
    "Video": {".mp4", ".mkv", ".mov", ".avi", ".wmv"},
    "Code": {".py", ".js", ".java", ".c", ".cpp", ".cs", ".rb", ".go", ".rs"},
}

window_style = """
QWidget {
    background-color: #0B0F14;
}
"""

card_style = """
QFrame {
    background-color: #121826;
    border-radius: 12px;
    border: 3px solid #263042;
    padding: 8px;
    margin: 0px;
}
QFrame:hover {
    border: 3px solid #364052;
}
"""

entry_style = """
QLineEdit {
    background-color: #1A2232;
    border: 1px solid #263042;
    border-radius: 6px;
    padding: 6px 8px;
    color: #E6EDF7;
    selection-background-color: #4F7CFF;
    width: 250px;
}

QLineEdit:focus {
    border: 1px solid #4F7CFF;
}

QLineEdit:disabled {
    background-color: #121826;
    color: #5B6472;
}
"""

btn_style = """
QPushButton {
    background-color: #4F7CFF;
    color: white;
    border-radius: 6px;
    margin: 6px 0px;
    padding: 6px 12px;
}
QPushButton:hover {
    background-color: #6B93FF;
}
QPushButton:disabled {
    background-color: #1B2A4D;
    color: #5B6472;
}
"""

title_style = """
QLabel {
    color: #E0E7F1;
    font-weight: 900;
    font-size: 36px;
    border: 0px;
    margin: 0px;
}
QLabel:hover {
    color: #FFFFFF;
}
"""

font = QFont("Inter", 11)
directory = ""

def match_ext(ext: str) -> str:
    ext = ext.lower()
    for group, exts in GROUPS.items():
        if ext in exts:
            return group
    return ext.lstrip('.') or "NoExt"

def sortfiles(folder: str) -> None:
    for name in os.listdir(folder):
        src = os.path.join(folder, name)
        if not os.path.isfile(src):
            continue
        ext = os.path.splitext(name)[1]
        group = match_ext(ext)
        dest = os.path.join(folder, group)
        if not os.path.exists(dest):
            os.makedirs(dest, exist_ok=True)
        path = os.path.join(dest, name)
        print(f"{name} -> {os.path.relpath(path, folder)}")
        shutil.copy2(src, path)

class MainWindow(QWidget):
    def __init__(self: QWidget) -> None: ...
    def getfiles(self) -> None: ...

    def __init__(self: QWidget) -> None:
        super().__init__()
        self.setFixedSize(1000, 600)
        self.setWindowTitle("File Organizer v1.0")
        self.setStyleSheet(window_style)

        main_layout = QGridLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(5, 5, 5, 5)

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setColor(QColor(0, 0, 0, 120))
        self.shadow.setOffset(8, 8)
        self.shadow.setBlurRadius(5)

        card_0 = QFrame(self)
        card_0.setStyleSheet(card_style)
        card_0.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        card_1 = QFrame(self)
        card_1.setStyleSheet(card_style)
        card_1.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        card_1.setGraphicsEffect(self.shadow)

        main_layout.addWidget(card_0, 0, 0, Qt.AlignmentFlag.AlignBottom)
        main_layout.addWidget(card_1, 1, 0, Qt.AlignmentFlag.AlignTop)

        # LAYOUT 0

        self.layout_0: QGridLayout = QGridLayout(card_0)

        self.title = QLabel(parent=card_0, text="FILE ORGANIZER")
        self.title.setStyleSheet(title_style)
        self.title.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.layout_0.addWidget(self.title)

        # LAYOUT 1

        self.layout_1: QGridLayout = QGridLayout(card_1)
        self.layout_1.setSpacing(8)

        self.filedialog = QFileDialog()

        self.entry_1 = QLineEdit(card_1)
        self.entry_1.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.entry_1.setStyleSheet(entry_style)
        self.entry_1.setPlaceholderText("Input folder path here..")
        
        self.btn_1 = QPushButton(parent=card_1, text="Sort files")
        self.btn_1.clicked.connect(lambda: sortfiles(self.entry_1.text() or self.dir))
        self.btn_1.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.btn_1.setStyleSheet(btn_style)

        self.btn_2 = QPushButton(parent=card_1, text="Choose folder")
        self.btn_2.clicked.connect(self.getfiles)
        self.btn_2.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.btn_2.setStyleSheet(btn_style)

        self.layout_1.addWidget(self.entry_1, 0, 0, 1, 2)
        self.layout_1.addWidget(self.btn_1, 1, 0)
        self.layout_1.addWidget(self.btn_2, 1, 1)

        self.show()

    def getfiles(self) -> None:
        self.dir = self.filedialog.getExistingDirectory()
        self.entry_1.setText(self.dir)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(font)

    root = MainWindow()
    
    app.exec()
