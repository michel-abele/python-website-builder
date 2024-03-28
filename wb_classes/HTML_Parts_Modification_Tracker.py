import json

from pathlib import Path

class HTML_Parts_Modification_Tracker:
    def __init__(self, parts_directory, json_file_path):
        self.parts_directory = Path(parts_directory)
        self.json_file_path = Path(json_file_path)

    # ==============================================================================================
    # track modifications
    def track_modifications(self):
        # checks if the JSON file exists
        if not self.json_file_path.exists():
            with self.json_file_path.open("w") as file:
                json.dump({}, file)

        # traverse the parts_directory recursively
        html_parts = {}
        for file_path in self.parts_directory.rglob("*.html"):
            relative_path = file_path.relative_to(self.parts_directory)
            relative_path = relative_path.with_suffix("")
            modification_date = file_path.stat().st_mtime
            html_parts[str(relative_path)] = modification_date

        # save the html parts directory to the JSON file
        with self.json_file_path.open("w") as file:
            json.dump(html_parts, file, indent=2)
