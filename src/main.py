from exporters.notes_exporter import NotesExporter
from templates.html_generator import HTMLGenerator
from utils.file_utils import FileUtils


def main():
    """Основная точка входа в приложение"""
    exporter = NotesExporter()
    notes = exporter.export_notes()

    if notes:
        html_generator = HTMLGenerator()
        file_utils = FileUtils()

        output_dir = "notes"
        file_utils.ensure_directory(output_dir)

        for note in notes:
            html_content = html_generator.create_note_html(note)
            file_utils.save_note(note["title"], html_content, output_dir)

        # Создаем индексную страницу
        index_html = html_generator.create_index_html(notes)
        file_utils.save_index(index_html, output_dir)

        print(f"Экспорт завершен успешно! Заметки сохранены в: {output_dir}")


if __name__ == "__main__":
    main()
