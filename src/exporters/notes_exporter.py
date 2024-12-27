import os
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from templates.html_generator import HTMLGenerator


@dataclass
class Attachment:
    filename: str
    content: bytes
    mime_type: str


@dataclass
class Note:
    title: str = ""
    content: str = ""
    html_content: str = ""
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None
    attachments: List[Attachment] = field(default_factory=list)


class NotesExporter:
    """Класс для экспорта заметок из Apple Notes"""

    def __init__(self, output_dir: str = "notes") -> None:
        self.output_dir: str = output_dir
        self.attachments_dir: str = os.path.join(output_dir, "attachments")
        self.html_generator: HTMLGenerator = HTMLGenerator()
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(self.attachments_dir, exist_ok=True)

    def export_notes(self) -> List[Dict[str, str]]:
        """
        Export notes from Apple Notes

        Returns:
            List[Dict[str, str]]: Список экспортированных заметок
        """
        try:
            notes: List[Dict[str, str]] = self._parse_applescript_output(
                self._get_notes_from_apple()
            )
            for note in notes:
                self._save_note(Note(title=note["title"], content=note["content"]))
            return notes
        except (subprocess.SubprocessError, OSError) as e:
            print(f"Export failed: {str(e)}")
            raise

    def get_notes_count(self) -> int:
        """Returns the number of notes"""
        return len(self._parse_applescript_output(self._get_notes_from_apple()))

    def _get_notes_from_apple(self) -> str:
        """Получает заметки из Apple Notes через AppleScript"""
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
                ["osascript", "-e", script], capture_output=True, text=True, check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error executing AppleScript: {e}")
            raise

    def _save_note(self, note: Note) -> None:
        """
        Сохраняет заметку в HTML файл

        Args:
            note: Заметка для сохранения
        """
        if not note.title:
            return

        # Сохраняем вложения
        for attachment in note.attachments:
            attachment_path = os.path.join(self.attachments_dir, attachment.filename)
            with open(attachment_path, "wb") as f:
                f.write(attachment.content)

        # Создаем HTML файл
        html_content = self.html_generator.create_note_html(
            {
                "title": note.title,
                "content": note.html_content or note.content,
                "created_date": note.created_date,
                "modified_date": note.modified_date,
                "attachments": [
                    {"filename": att.filename, "mime_type": att.mime_type}
                    for att in note.attachments
                ],
            }
        )

        filename = os.path.join(
            self.output_dir, f"{self._create_safe_filename(note.title)}.html"
        )
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)

    def _parse_applescript_output(self, output: str) -> List[Dict[str, str]]:
        """
        Парсит вывод AppleScript и преобразует его в список заметок

        Args:
            output: Вывод AppleScript

        Returns:
            List[Dict[str, str]]: Список заметок
        """
        notes: List[Dict[str, str]] = []
        current_note: Optional[Dict[str, str]] = None

        for line in output.strip().split("\n"):
            line = line.strip()

            if line == "---END_NOTE---" and current_note is not None:
                notes.append(current_note)
                current_note = None
                continue

            if line.startswith("title:"):
                current_note = {
                    "title": line[6:].strip(),
                    "content": "",
                    "html_content": "",
                    "attachments": [],
                    "created_date": None,
                    "modified_date": None,
                }
            elif current_note is not None:
                if line.startswith("content:"):
                    content = line[8:].strip()
                    current_note["content"] = content
                    # Конвертируем обычный текст в базовый HTML
                    current_note["html_content"] = content.replace("\n", "<br>")
                elif line.startswith("created:"):
                    current_note["created_date"] = line[8:].strip()
                elif line.startswith("modified:"):
                    current_note["modified_date"] = line[9:].strip()
                elif line.startswith("attachment:"):
                    attachment_data = line[11:].strip().split("|")
                    if len(attachment_data) == 2:
                        current_note["attachments"].append(
                            {"id": attachment_data[0], "filename": attachment_data[1]}
                        )

        if current_note is not None:
            notes.append(current_note)

        return notes

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
