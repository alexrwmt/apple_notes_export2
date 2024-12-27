import os
import subprocess
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Note:
    title: str = ""
    content: str = ""


class NotesExporter:
    """Класс для экспорта заметок из Apple Notes"""

    def __init__(self, output_dir: str = "notes") -> None:
        self.output_dir: str = output_dir
        os.makedirs(output_dir, exist_ok=True)

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
        # TODO: Реализовать получение заметок через AppleScript
        return ""  # Временная заглушка

    def _save_note(self, note: Note) -> None:
        """
        Сохраняет заметку в файл

        Args:
            note: Заметка для сохранения
        """
        if not note.title:
            return

        filename = f"{self.output_dir}/{note.title}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Title: {note.title}\n\n{note.content}")

    def _parse_applescript_output(self, output: str) -> List[Dict[str, str]]:
        """
        Парсит вывод AppleScript и преобразует его в список словарей

        Args:
            output: Вывод AppleScript

        Returns:
            List[Dict[str, str]]: Список заметок
        """
        notes: List[Dict[str, str]] = []
        lines = output.strip().split("\n")

        current_note: Dict[str, str] = {}
        for line in lines:
            line = line.strip()
            if line.startswith("title:"):
                if current_note and "title" in current_note:
                    notes.append(current_note)
                current_note = {"title": line[6:].strip(), "content": ""}
            elif line.startswith("content:") and current_note:
                current_note["content"] = line[8:].strip()

        if current_note and "title" in current_note:
            notes.append(current_note)

        return notes
