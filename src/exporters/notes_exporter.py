import subprocess
from typing import List, Dict

class NotesExporter:
    """Класс для экспорта заметок из Apple Notes"""
    
    def export_notes(self) -> List[Dict[str, str]]:
        """
        Экспортирует заметки из Apple Notes
        
        Returns:
            List[Dict[str, str]]: Список заметок в формате [{'title': str, 'content': str}]
        """
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
            return self._parse_applescript_output(result.stderr)
            
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return []

    def _parse_applescript_output(self, output: str) -> List[Dict[str, str]]:
        """
        Парсит вывод AppleScript и преобразует его в список словарей
        
        Args:
            output: Вывод AppleScript
            
        Returns:
            List[Dict[str, str]]: Список заметок
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
