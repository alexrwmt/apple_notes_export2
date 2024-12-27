import os
import sys

# Добавляем директорию src в PYTHONPATH
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
sys.path.insert(0, src_path)

# Импортируем и запускаем main
from main import main

if __name__ == "__main__":
    main() 