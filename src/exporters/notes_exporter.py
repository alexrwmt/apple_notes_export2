import os
import subprocess
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
import logging
import shutil

from templates.html_generator import HTMLGenerator


@dataclass
class Note:
    title: str = ""
    content: str = ""
    html_content: str = ""
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None


class NotesExporter:
    """Класс для экспорта заметок из Apple Notes"""

    def __init__(self, output_dir: str = "notes") -> None:
        # Сначала сохраняем путь к директории
        self.output_dir: str = output_dir
        self.attachments_dir: str = os.path.join(output_dir, "attachments")
        
        # Создаем директории до настройки логгера
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(self.attachments_dir, exist_ok=True)

        # Создаем директорию для статических файлов
        static_dir = os.path.join(output_dir, "static", "css")
        os.makedirs(static_dir, exist_ok=True)
        
        # Копируем CSS файл
        src_css = os.path.join(os.path.dirname(__file__), "..", "static", "css", "style.css")
        dst_css = os.path.join(static_dir, "style.css")
        shutil.copy2(src_css, dst_css)

        # Теперь настраиваем логгер, когда директория уже существует
        self.logger = logging.getLogger(__name__)
        
        log_file = os.path.join(output_dir, 'notes_export.log')
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        console_handler = logging.StreamHandler()
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        self.logger.setLevel(logging.DEBUG)
        
        # Инициализируем остальные компоненты
        self.html_generator: HTMLGenerator = HTMLGenerator()

    def export_notes(self) -> List[Dict[str, str]]:
        """
        Export notes from Apple Notes

        Returns:
            List[Dict[str, str]]: Список экспортированных заметок
        """
        try:
            print("\nПолучаем заметки из Apple Notes...")
            raw_output = self._get_notes_from_apple()
            print(f"\nПолучен вывод AppleScript:\n{raw_output}\n")
            
            notes: List[Dict[str, str]] = self._parse_applescript_output(raw_output)
            print(f"\nРаспарсено {len(notes)} заметок:")
            
            for i, note in enumerate(notes, 1):
                print(f"\n=== Заметка {i} ===")
                print(f"Заголовок: {note['title']}")
                print(f"Контент: {note['content'][:100]}..." if len(note['content']) > 100 else f"Контент: {note['content']}")
                print(f"Дата создания: {note['created']}")
                print(f"Дата изменения: {note['modified']}")
                print(f"Количество вложений: {len(note['attachments'])}")
                
                self._save_note(Note(
                    title=note["title"], 
                    content=note["content"],
                    html_content=note.get("html_content", ""),
                    created_date=note.get("created"),
                    modified_date=note.get("modified")
                ))

            # Генерируем индексный файл
            index_html = self.html_generator.create_index_html(notes)
            index_path = os.path.join(self.output_dir, "index.html")
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(index_html)
            
            self.logger.info(f"Generated index.html with {len(notes)} notes")
            return notes
        
        except (subprocess.SubprocessError, OSError) as e:
            self.logger.error(f"Export failed: {str(e)}")
            raise

    def get_notes_count(self) -> int:
        """Returns the number of notes"""
        return len(self._parse_applescript_output(self._get_notes_from_apple()))

    def _get_notes_from_apple(self) -> str:
        """Получает заметки из Apple Notes через AppleScript в формате JSON"""
        script = """
            tell application "Notes"
                set allNotes to every note
                set noteData to ""
                repeat with currentNote in allNotes
                    set noteData to noteData & "title:" & name of currentNote & "\n"
                    set noteData to noteData & "created:" & creation date of currentNote & "\n"
                    set noteData to noteData & "modified:" & modification date of currentNote & "\n"
                    set noteData to noteData & "content:" & body of currentNote & "\n"
                    -- Получаем вложения
                    set attachmentData to ""
                    set noteAttachments to attachments of currentNote
                    repeat with currentAttachment in noteAttachments
                        set attachmentData to attachmentData & "attachment:" & id of currentAttachment & "|" & name of currentAttachment & "\n"
                    end repeat
                    set noteData to noteData & attachmentData & "---END_NOTE---\n"
                end repeat
                return noteData
            end tell
        """

        try:
            result = subprocess.run(
                ["osascript", "-e", script], 
                capture_output=True, 
                text=True, 
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error executing AppleScript: {e}")
            self.logger.error(f"Error output: {e.stderr}")
            raise

    def _save_note(self, note: Note) -> None:
        """
        Сохраняет заметку в HTML файл

        Args:
            note: Заметка для сохранения
        """
        if not note.title:
            return

        # Создаем HTML файл
        html_content = self.html_generator.create_note_html(
            {
                "title": note.title,
                "content": note.html_content or note.content,
                "created_date": note.created_date,
                "modified_date": note.modified_date
            }
        )

        filename = os.path.join(
            self.output_dir, f"{self._create_safe_filename(note.title)}.html"
        )
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)

    def _parse_applescript_output(self, output: str) -> List[Dict[str, str]]:
        """
        Парсит JSON вывод AppleScript и выполняет валидацию данных
        """
        import json
        
        try:
            notes = json.loads(output)
            processed_notes = []
            
            for note in notes:
                processed_note = {
                    'title': note['title'],
                    'content': note['content'],
                    'created': note['created'],
                    'modified': note['modified']
                }
                processed_notes.append(processed_note)
                
            return processed_notes
            
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON Parse Error: {str(e)}")
            raise

    def _get_mime_type(self, filename: str) -> str:
        """Определяет MIME-тип файла по расширению"""
        import mimetypes
        mime_type, _ = mimetypes.guess_type(filename)
        return mime_type or 'application/octet-stream'

    def _get_attachment_content(self, attachment_id: str) -> bytes:
        """Получает содержимое вложения через AppleScript"""
        script = f'''
        tell application "Notes"
            set theAttachment to attachment id "{attachment_id}"
            return theAttachment's data
        end tell
        '''
        
        try:
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error getting attachment content: {str(e)}")
            return bytes()

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
