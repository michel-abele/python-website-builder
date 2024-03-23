import os
import shutil

def process_js_files(source_dir, target_dir, temp_dir):
    os.makedirs(target_dir, exist_ok=True)

    for filename in os.listdir(source_dir):
        source_path = os.path.join(source_dir, filename)
        temp_path = os.path.join(temp_dir, filename)

        if os.path.getsize(source_path) == 0:
            continue

        with open(source_path, "r") as file:
            content = file.read()
            if "import" in content:
                os.makedirs(temp_dir, exist_ok=True)

                shutil.copy(source_path, temp_path)

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
                
                with open(temp_path, "w") as file:
                    file.write("\n".join(modified_content))

                shutil.copy(temp_path, target_dir)

                os.remove(temp_path)
            else:
                shutil.copy(source_path, target_dir)
