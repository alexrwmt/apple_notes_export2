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
        attachments_html = self._generate_attachments_html(note.get("attachments", []))
        dates_html = self._generate_dates_html(
            note.get("created_date"), note.get("modified_date")
        )

        return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{note['title']}</title>
   
</head>
<body>
    <h1>{note['title']}</h1>
    {dates_html}
    <div class="content">{note['content']}</div>
    {attachments_html}
</body>
</html>"""

    def _generate_attachments_html(self, attachments: List[Dict]) -> str:
        """Генерирует HTML для вложений"""
        if not attachments:
            return ""

        attachments_list = []
        for att in attachments:
            filename = att["filename"]
            mime_type = att.get("mime_type", "").lower()

            if mime_type.startswith("image/"):
                attachments_list.append(
                    f"""
                    <div class="attachment-item">
                        <img src="../attachments/{filename}" alt="{filename}">
                    </div>"""
                )
            else:
                attachments_list.append(
                    f"""
                    <div class="attachment-item">
                        <a href="../attachments/{filename}">{filename}</a>
                    </div>"""
                )

        return f"""
        <div class="attachments">
            <h2>Вложения</h2>
            {"".join(attachments_list)}
        </div>"""

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
            safe_filename = "".join(
                c if c.isalnum() or c in ("-", "_") else "_" for c in note["title"]
            ).lower()
            
            notes_list.append(
                f"""
                <li>
                    <div class="note-item">
                        <a href="{safe_filename}.html">{note['title']}</a>
                        <div class="note-metadata">
                            <span>Создано: {note.get('created', 'Нет даты')}</span>
                            <span>Изменено: {note.get('modified', 'Нет даты')}</span>
                            <span>Вложений: {len(note.get('attachments', []))}</span>
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
