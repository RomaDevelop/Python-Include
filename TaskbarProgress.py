import sys
from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton
from PySide6.QtCore import QTimer

try:
    import win32com.client
    import pythoncom
except ImportError:
    print("Ошибка: Библиотека pywin32 не найдена. Выполните: pip install pywin32")


class TaskbarProgress:
    def __init__(self, window: QWidget, minimum: int = 0, maximum: int = 1000):
        self.window = window
        self.maximum = maximum
        self.current_value = minimum
        self._taskbar = None

        # Константы ITaskbarList3
        self.TBPF_NORMAL = 0x2
        self.TBPF_NOPROGRESS = 0x0

        try:
            # Инициализируем COM
            pythoncom.CoInitialize()
            # Создаем объект через Dispatch (используем CLSID напрямую)
            # Это самый стабильный способ в pywin32
            self._taskbar = win32com.client.Dispatch("{56FDF344-FD6D-11D0-958A-006097C9A090}")
            self._taskbar.HrInit()
        except Exception as e:
            print(f"Ошибка инициализации Taskbar: {e}")

    def set_value(self, value: int):
        self.current_value = value
        print(f"Вызов set_value: {self.current_value}/{self.maximum}")

        if not self._taskbar:
            print("Ошибка: Интерфейс Taskbar не создан.")
            return

        try:
            # HWND в PySide6 извлекается через winId()
            hwnd = self.window.winId()

            if self.current_value >= self.maximum:
                self._taskbar.SetProgressState(hwnd, self.TBPF_NOPROGRESS)
            else:
                self._taskbar.SetProgressState(hwnd, self.TBPF_NORMAL)
                self._taskbar.SetProgressValue(hwnd, self.current_value, self.maximum)
        except Exception as e:
            print(f"Ошибка выполнения SetProgress: {e}")

    def add_points(self, count: int):
        self.set_value(self.current_value + count)


# Проверочный запуск
if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(300, 100)
    w.show()  # Окно ДОЛЖНО быть показано для получения HWND

    tp = TaskbarProgress(w)

    # Чтобы увидеть результат сразу (нужна небольшая задержка, пока Windows подцепит окно)
    QTimer.singleShot(1000, lambda: tp.set_value(500))

    sys.exit(app.exec())