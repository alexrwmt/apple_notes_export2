import subprocess
import os
from datetime import datetime

def export_notes(output_dir="notes"):
    """
    Export notes from Apple Notes using AppleScript
    
    Parameters:
    output_dir (str): Directory to save exported notes
    """
    # Создаем директорию, если она не существует
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    
    applescript = '''
    try
        tell application "Notes"
            log "Starting Notes export..."
            set noteCount to count of notes
            log "Total notes found: " & noteCount
            
            set allNotes to every note
            repeat with currentNote in allNotes
                set noteContent to body of currentNote
                set noteTitle to name of currentNote
                log "title: " & noteTitle
                log "content: " & noteContent
            end repeat
            log "Export completed"
        end tell
    on error errMsg
        log "Error: " & errMsg
        error errMsg
    end try
    '''
    
    try:
        print("Executing AppleScript to export notes...")
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, 
                              text=True)
        
        # Используем stderr вместо stdout, так как AppleScript пишет в лог
        notes_data = parse_applescript_output(result.stderr)
        print(f"\nFound {len(notes_data)} notes:")
        print("=" * 80)
        
        # Выводим заголовки и первые 5 строк каждой заметки
        for i, note in enumerate(notes_data, 1):
            print(f"{i}. {note['title']}")
            
            # Получаем первые 5 строк контента
            preview_lines = note['content'].split('\n')[:5]
            preview = '\n   '.join(line.strip() for line in preview_lines if line.strip())
            if preview:
                print(f"   {preview}")
                if len(note['content'].split('\n')) > 5:
                    print("   ...")
            print("-" * 80)
        
        print()  # Пустая строка для разделения
        
        # Сохраняем каждую заметку
        for i, note in enumerate(notes_data, 1):
            filename = create_safe_filename(note['title'])
            file_path = os.path.join(output_dir, f"{filename}.html")
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(create_html_note(note['title'], note['content']))
            print(f"Saved note {i}/{len(notes_data)}: {filename}.html")
        
        # Создаем индексную страницу
        index_path = os.path.join(output_dir, "index.html")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(create_index_page(notes_data))
        print(f"Created index page: {index_path}")
        
        print(f"\nExport completed successfully!")
        print(f"Total notes exported: {len(notes_data)}")
        print(f"Output directory: {os.path.abspath(output_dir)}")
            
    except Exception as e:
        print(f"Error occurred: {str(e)}")

def parse_applescript_output(output):
    """
    Парсит вывод AppleScript и преобразует его в список словарей
    """
    notes = []
    lines = output.strip().split('\n')
    
    current_note = None
    for line in lines:
        line = line.strip()
        if line.startswith('title:'):
            # Если есть предыдущая заметка, добавляем её в список
            if current_note:
                notes.append(current_note)
            # Создаем новую заметку
            current_note = {
                'title': line[6:].strip(),
                'content': ''
            }
        elif line.startswith('content:') and current_note is not None:
            # Добавляем контент к текущей заметке
            current_note['content'] = line[8:].strip()
    
    # Добавляем последнюю заметку
    if current_note:
        notes.append(current_note)
    
    return notes

def create_html_note(title, content):
    """
    Создает HTML разметку для заметки
    
    Parameters:
    title (str): Заголовок заметки
    content (str): Содержимое заметки
    
    Returns:
    str: HTML разметка заметки
    """
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
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
    <h1>{title}</h1>
    {content}
</body>
</html>"""

def create_index_page(notes):
    """
    Создает индексную страницу со списком всех заметок
    
    Parameters:
    notes (list): Список словарей с заметками
    
    Returns:
    str: HTML разметка индексной страницы
    """
    notes_list = "\n".join([
        f'<li><a href="{create_safe_filename(note["title"])}.html">{note["title"]}</a></li>'
        for note in notes
    ])
    
    return f"""
<!DOCTYPE html>
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
</html>
"""

def create_safe_filename(title):
    """
    Создает безопасное имя файла из заголовка заметки
    
    Parameters:
    title (str): Заголовок заметки
    
    Returns:
    str: Безопасное имя файла
    """
    # Заменяем недопустимые символы на underscore
    safe_filename = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in title)
    return safe_filename.lower()

if __name__ == "__main__":
    export_notes()
