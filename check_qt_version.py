import PySide6

# 1. Версия самого пакета PySide6 (обычно совпадает с версией Qt для компиляции)
print(f"PySide6 version: {PySide6.__version__}")

# 2. Версия Qt, которая запущена в данный момент (рекомендуемый способ)
from PySide6.QtCore import qVersion
print(f"Running Qt version: {qVersion()}")