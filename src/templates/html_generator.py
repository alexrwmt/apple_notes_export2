from typing import Dict, List


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
        return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{note['title']}</title>
    <style>
        body {{ 
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1 {{ color: #333; }}
        .content {{
            margin-top: 20px;
            white-space: pre-wrap;
        }}
    </style>
</head>
<body>
    <h1>{note['title']}</h1>
    <div class="content">{note['content']}</div>
</body>
</html>"""

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
