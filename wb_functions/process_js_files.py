import os
import shutil

def process_js_files(source_dir, target_dir, temp_dir):

    # Erstelle das Zielverzeichnis, falls es nicht existiert
    os.makedirs(target_dir, exist_ok=True)

    # Kopiere JavaScript-Dateien vom Quellverzeichnis ins temporäre Verzeichnis
    for filename in os.listdir(source_dir):
        source_path = os.path.join(source_dir, filename)
        temp_path = os.path.join(temp_dir, filename)

        # Überspringe leere Dateien
        if os.path.getsize(source_path) == 0:
            continue

        # Überprüfe, ob die Datei andere JavaScript-Dateien importiert
        with open(source_path, "r") as file:
            content = file.read()
            if "import" in content:
                # Erstelle das temporäre Verzeichnis, falls es nicht existiert
                os.makedirs(temp_dir, exist_ok=True)

                # Kopiere die Quelldatei ins temporäre Verzeichnis
                shutil.copy(source_path, temp_path)

                # Ersetze den Importbefehl durch den Inhalt der importierten Datei
                lines = content.split("\n")
                modified_content = []
                for line in lines:
                    if line.startswith("import"):
                        imported_file = line.split(" ")[1].strip()
                        imported_file_path = os.path.join(source_dir, imported_file + ".js")
                        with open(imported_file_path, "r") as imported_file:
                            imported_content = imported_file.read()
                            modified_content.append(imported_content)
                    else:
                        modified_content.append(line)
                
                # Schreibe den modifizierten Inhalt in die temporäre Datei
                with open(temp_path, "w") as file:
                    file.write("\n".join(modified_content))

                # Kopiere die modifizierte temporäre Datei ins Zielverzeichnis
                shutil.copy(temp_path, target_dir)

                # Entferne die temporäre Datei
                os.remove(temp_path)
            else:
                # Kopiere die Datei direkt ins Zielverzeichnis
                shutil.copy(source_path, target_dir)
