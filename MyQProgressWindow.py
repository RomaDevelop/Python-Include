from PySide6.QtWidgets import QWidget, QVBoxLayout, QProgressBar
from PySide6.QtCore import QByteArray, Qt

class MyQProgressWindow(QWidget):
    geo = QByteArray()

    def __init__(self, parent: QWidget, minimum: int = 0, maximum: int = 1000):
        super().__init__()

        parent.destroyed.connect(self.deleteLater)

        self.setWindowFlags(
            Qt.WindowType.Tool |
            Qt.WindowType.WindowStaysOnTopHint
        )

        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        self.setWindowTitle("Active downloads progress")
        
        layout = QVBoxLayout(self)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(minimum, maximum)
        self.progress_bar.setValue(minimum)
        layout.addWidget(self.progress_bar)

    def set_value(self, value: int):
        if not self.isVisible():
            if MyQProgressWindow.geo and not MyQProgressWindow.geo.isEmpty():
                self.restoreGeometry(MyQProgressWindow.geo)
            self.show()

        self.progress_bar.setValue(value)

        if self.progress_bar.value() >= self.progress_bar.maximum():
            self.adjustSize()

    def add_points(self, count: int):
        self.set_value(self.progress_bar.value() + count)

    def moveEvent(self, event):
        MyQProgressWindow.geo = self.saveGeometry()
        super().moveEvent(event)

    def resizeEvent(self, event):
        MyQProgressWindow.geo = self.saveGeometry()
        super().resizeEvent(event)