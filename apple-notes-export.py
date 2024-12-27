import pyicloud
import json
from datetime import datetime
import os

def export_notes(apple_id, password, output_dir="exported_notes"):
    """
    Export notes from Apple Notes using iCloud API
    
    Parameters:
    apple_id (str): Apple ID (email)
    password (str): Apple ID password
    output_dir (str): Directory to save exported notes
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        # Connect to iCloud
        api = pyicloud.PyiCloudService(apple_id, password)
        
        # Ensure we're authenticated
        if api.requires_2fa:
            print("Two-factor authentication required. Please check your devices and enter the code:")
            code = input("Enter 2FA code: ")
            api.validate_2fa_code(code)
        
        # Get notes
        notes = api.notes.all()
        
        # Export each note
        for i, note in enumerate(notes):
            # Create safe filename
            filename = f"note_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Export as markdown
            with open(f"{output_dir}/{filename}.md", "w", encoding="utf-8") as f:
                f.write(f"# {note.title}\n\n")
                f.write(note.content)
            
            # Also save metadata as JSON
            metadata = {
                "title": note.title,
                "created": str(note.created),
                "modified": str(note.modified),
                "author": note.author
            }
            
            with open(f"{output_dir}/{filename}_metadata.json", "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)
        
        print(f"Successfully exported {len(notes)} notes to {output_dir}")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    apple_id = input("Enter your Apple ID: ")
    password = input("Enter your password: ")
    export_notes(apple_id, password)
