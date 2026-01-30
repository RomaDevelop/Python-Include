
from PySide6.QtCore import QSettings

class MyQSettings(QSettings):
    def smart_value(self, key, default_value):
        return self.value(key, defaultValue=default_value, type=type(default_value))

class Setting:
    def __init__(self, name: str, value):
        self.name = name
        self.value = value

    def set(self, value):
        self.value = value

class SettingsList(list):
    def __init__(self, iterable):
        # Проверяем все элементы при инициализации списка
        for item in iterable:
            self._validate_is_setting(item)
        super().__init__(iterable)

    @staticmethod
    def _validate_is_setting(item):
        if not isinstance(item, Setting):
            raise TypeError(f"Элемент должен быть типа Setting, а не {type(item).__name__}")

    def __setitem__(self, index, value):
        # Проверяем, что по этому индексу реально лежит Setting
        target = self[index]
        if isinstance(target, Setting):
            # Обновляем значение внутри объекта
            target.value = value
        else:
            # На случай, если проверка при инициализации была обойдена
            raise TypeError("Попытка записи в объект, который не является Setting")

    def append(self, item):
        self._validate_is_setting(item)
        super().append(item)

    def insert(self, index, item):
        self._validate_is_setting(item)
        super().insert(index, item)