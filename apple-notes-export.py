import subprocess
import os
from datetime import datetime

def export_notes(output_dir="exported_notes"):
    """
    Export notes from Apple Notes using AppleScript
    
    Parameters:
    output_dir (str): Directory to save exported notes
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    applescript = '''
    tell application "Notes"
        set allNotes to every note
        repeat with currentNote in allNotes
            set noteContent to body of currentNote
            set noteTitle to name of currentNote
            log "title: " & noteTitle
            log "content: " & noteContent
        end repeat
    end tell
    '''
    
    try:
        # Выполняем AppleScript
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, 
                              text=True)
        
        print("Raw output:", result.stdout)  # Отладочный вывод
        print("Error output:", result.stderr)  # Отладочный вывод
        print("Return code:", result.returncode)  # Отладочный вывод
        
        if result.returncode == 0:
            # Обрабатываем каждую заметку
            notes_data = parse_applescript_output(result.stdout)
            
            for i, note in enumerate(notes_data):
                # Создаем безопасное имя файла
                filename = f"note_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                # Сохраняем как markdown
                with open(f"{output_dir}/{filename}.md", "w", encoding="utf-8") as f:
                    f.write(f"# {note['title']}\n\n")
                    f.write(note['content'])
                
            print(f"Successfully exported {len(notes_data)} notes to {output_dir}")
        else:
            print(f"Error: {result.stderr}")
            
    except Exception as e:
        print(f"Error occurred: {str(e)}")

def parse_applescript_output(output):
    """
    Парсит вывод AppleScript и преобразует его в список словарей
    
    Parameters:
    output (str): Вывод AppleScript
    
    Returns:
    list: Список словарей с заметками [{title: str, content: str}, ...]
    """
    notes = []
    
    # Убираем лишние символы и разбиваем на строки
    lines = output.strip().split('\n')
    
    current_note = {}
    for line in lines:
        line = line.strip()
        if line.startswith('title:'):
            if current_note:
                notes.append(current_note)
            current_note = {'title': line[6:].strip(), 'content': ''}
        elif line.startswith('content:'):
            current_note['content'] = line[8:].strip()
    
    # Добавляем последнюю заметку
    if current_note:
        notes.append(current_note)
    
    return notes

if __name__ == "__main__":
    export_notes()
