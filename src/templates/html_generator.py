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
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1 {{ 
            color: #1a1a1a;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }}
        .content {{
            margin: 20px 0;
            white-space: pre-wrap;
        }}
        .metadata {{
            color: #666;
            font-size: 0.9em;
            margin: 10px 0;
        }}
        .attachments {{
            margin-top: 20px;
            padding: 15px;
            background: #f5f5f5;
            border-radius: 5px;
        }}
        .attachments h2 {{
            font-size: 1.2em;
            margin-top: 0;
        }}
        .attachment-item {{
            display: flex;
            align-items: center;
            margin: 10px 0;
        }}
        .attachment-item img {{
            max-width: 100%;
            height: auto;
            margin: 10px 0;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f5f5f5;
        }}
    </style>
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

    def create_index_html(self, notes: List[Dict[str, str]]) -> str:
        """
        Создает индексную HTML страницу со списком всех заметок

        Args:
            notes: Список заметок

        Returns:
            str: HTML разметка индексной страницы
        """
        notes_list = "\n".join(
            [
                "<li>"
                f'<a href="{self._create_safe_filename(note["title"])}.html">'
                f'{note["title"]}'
                "</a></li>"
                for note in notes
            ]
        )

        return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Список заметок</title>
    <style>
        body {{ 
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1 {{ color: #333; }}
        ul {{ 
            list-style-type: none;
            padding: 0;
        }}
        li {{ 
            margin: 10px 0;
            padding: 10px;
            border-bottom: 1px solid #eee;
        }}
        a {{ 
            color: #0066cc;
            text-decoration: none;
        }}
        a:hover {{ 
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <h1>Список заметок</h1>
    <ul>
        {notes_list}
    </ul>
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
