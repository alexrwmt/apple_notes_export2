import os
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
        return "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in title).lower()
    
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
