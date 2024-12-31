from datetime import datetime
from typing import Dict, List


class HTMLGenerator:
    """Класс для генерации HTML страниц"""

    def create_note_html(self, note: Dict) -> str:
        """
        Создает HTML разметку для отдельной заметки

        Args:
            note: Словарь с данными заметки

        Returns:
            str: HTML разметка заметки
        """
        dates_html = self._generate_dates_html(
            note.get("created_date"), note.get("modified_date")
        )

        return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{note['title']}</title>
    <link rel="stylesheet" href="../static/css/style.css">
</head>
<body>
    <h1>{note['title']}</h1>
    {dates_html}
    <div class="content">{note['content']}</div>
</body>
</html>"""

    def _generate_dates_html(self, created_date, modified_date) -> str:
        """Генерирует HTML для дат создания и изменения"""
        dates = []
        if created_date:
            dates.append(f"Создано: {created_date}")
        if modified_date:
            dates.append(f"Изменено: {modified_date}")

        if dates:
            return f'<div class="metadata">{" | ".join(dates)}</div>'
        return ""

    def create_index_html(self, notes: List[Dict]) -> str:
        """
        Создает HTML страницу со списком всех заметок
        
        Args:
            notes: Список заметок
            
        Returns:
            str: HTML разметка индексной страницы
        """
        notes_list = []
        for note in notes:
            safe_filename = self._create_safe_filename(note["title"])
            
            notes_list.append(
                f"""
                <li>
                    <div class="note-item">
                        <a href="{safe_filename}.html">{note['title']}</a>
                        <div class="note-metadata">
                            <span>Создано: {note.get('created', 'Нет даты')}</span>
                            <span>Изменено: {note.get('modified', 'Нет даты')}</span>
                        </div>
                    </div>
                </li>"""
            )

        return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Список заметок</title>
    <link rel="stylesheet" href="static/css/style.css">
</head>
<body>
    <h1>Список заметок</h1>
    <div class="notes-container">
        <ul class="notes-list">
            {"".join(notes_list)}
        </ul>
    </div>
</body>
</html>"""

    def _create_safe_filename(self, title: str) -> str:
        """
        Создает безопасное имя файла из заголовка

        Args:
            title: Исходный заголовок

        Returns:
            str: Безопасное имя файла
        """
        return "".join(
            c if c.isalnum() or c in ("-", "_") else "_" for c in title
        ).lower()
