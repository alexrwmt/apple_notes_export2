from exporters.notes_exporter import NotesExporter
from templates.html_generator import HTMLGenerator
from utils.file_utils import FileUtils


def main():
    exporter = NotesExporter()
    notes = exporter.export_notes()

    if notes:
        print(f"Экспортировано {len(notes)} заметок")


if __name__ == "__main__":
    main()
