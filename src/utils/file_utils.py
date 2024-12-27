import os
from typing import Optional


class FileUtils:

    def ensure_directory(self, directory: str) -> None:
        if not os.path.exists(directory):
            os.makedirs(directory)

    def create_safe_filename(self, title: str) -> str:
        return "".join(
            c if c.isalnum() or c in ("-", "_") else "_" for c in title
        ).lower()

    def save_note(self, title: str, content: str, output_dir: str) -> None:
        filename = self.create_safe_filename(title)
        filepath = os.path.join(output_dir, f"{filename}.html")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    def save_index(self, content: str, output_dir: str) -> None:
        filepath = os.path.join(output_dir, "index.html")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
