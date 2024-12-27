import os
import sys

def create_directory(path):
    """Создает директорию, если она не существует"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"✓ Создана директория: {path}")

def create_file(path, content=""):
    """Создает файл с указанным содержимым"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Создан файл: {path}")

def setup_project():
    """Создает структуру проекта"""
    # Создаем основные директории
    directories = [
        'src',
        'src/exporters',
        'src/templates',
        'src/utils',
        'tests'
    ]
    
    for directory in directories:
        create_directory(directory)
        # Создаем __init__.py в каждой директории Python
        create_file(os.path.join(directory, '__init__.py'))

    # Создаем основные файлы
    create_file('requirements.txt', '''# Project dependencies
# Add your dependencies here
''')

    create_file('README.md', '''# Apple Notes Sync

Проект для экспорта заметок из Apple Notes.

## Структура проекта

```
apple-notes-sync/
├── src/
│   ├── main.py              # точка входа в приложение
│   ├── exporters/           # модуль для экспорта
│   ├── templates/           # модуль для HTML шаблонов
│   └── utils/               # вспомогательные функции
├── requirements.txt         # зависимости проекта
└── tests/                  # тесты
```

## Установка

1. Клонируйте репозиторий
2. Установите зависимости: `pip install -r requirements.txt`

## Использование

Запустите `main.py` для экспорта заметок:
```python
python src/main.py
```
''')

    create_file('.gitignore', '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
notes/
''')

    # Создаем базовые файлы с кодом
    create_file('src/main.py', '''from exporters.notes_exporter import NotesExporter
from templates.html_generator import HTMLGenerator
from utils.file_utils import FileUtils

def main():
    """Основная точка входа в приложение"""
    exporter = NotesExporter()
    notes = exporter.export_notes()
    
    if notes:
        html_generator = HTMLGenerator()
        file_utils = FileUtils()
        
        output_dir = "notes"
        file_utils.ensure_directory(output_dir)
        
        for note in notes:
            html_content = html_generator.create_note_html(note)
            file_utils.save_note(note['title'], html_content, output_dir)
        
        # Создаем индексную страницу
        index_html = html_generator.create_index_html(notes)
        file_utils.save_index(index_html, output_dir)
        
        print(f"Экспорт завершен успешно! Заметки сохранены в: {output_dir}")

if __name__ == "__main__":
    main()
''')

    create_file('src/exporters/notes_exporter.py', '''import subprocess
from typing import List, Dict

class NotesExporter:
    """Класс для экспорта заметок из Apple Notes"""
    
    def export_notes(self) -> List[Dict[str, str]]:
        """
        Экспортирует заметки из Apple Notes
        
        Returns:
            List[Dict[str, str]]: Список заметок в формате [{'title': str, 'content': str}]
        """
        # TODO: Перенести код экспорта из основного файла
        pass
''')

    create_file('src/templates/html_generator.py', '''from typing import List, Dict

class HTMLGenerator:
    """Класс для генерации HTML страниц"""
    
    def create_note_html(self, note: Dict[str, str]) -> str:
        """
        Создает HTML разметку для отдельной заметки
        
        Args:
            note: Словарь с данными заметки
        
        Returns:
            str: HTML разметка заметки
        """
        # TODO: Перенести код генерации HTML из основного файла
        pass
    
    def create_index_html(self, notes: List[Dict[str, str]]) -> str:
        """
        Создает индексную HTML страницу со списком всех заметок
        
        Args:
            notes: Список заметок
        
        Returns:
            str: HTML разметка индексной страницы
        """
        # TODO: Перенести код генерации индекса из основного файла
        pass
''')

    create_file('src/utils/file_utils.py', '''import os
from typing import Optional

class FileUtils:
    """Утилиты для работы с файлами"""
    
    def ensure_directory(self, directory: str) -> None:
        """
        Создает директорию, если она не существует
        
        Args:
            directory: Путь к директории
        """
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    def create_safe_filename(self, title: str) -> str:
        """
        Создает безопасное имя файла из заголовка
        
        Args:
            title: Исходный заголовок
        
        Returns:
            str: Безопасное имя файла
        """
        # TODO: Перенести код создания имени файла из основного файла
        pass
    
    def save_note(self, title: str, content: str, output_dir: str) -> None:
        """
        Сохраняет заметку в файл
        
        Args:
            title: Заголовок заметки
            content: HTML содержимое заметки
            output_dir: Директория для сохранения
        """
        filename = self.create_safe_filename(title)
        filepath = os.path.join(output_dir, f"{filename}.html")
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
    
    def save_index(self, content: str, output_dir: str) -> None:
        """
        Сохраняет индексную страницу
        
        Args:
            content: HTML содержимое индексной страницы
            output_dir: Директория для сохранения
        """
        filepath = os.path.join(output_dir, "index.html")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
''')

if __name__ == "__main__":
    setup_project()
    print("\n✨ Структура проекта успешно создана!") 