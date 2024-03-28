import os
import shutil
import sass
import sys

def process_scss_files(source_dir, target_dir, temp_dir):
    os.makedirs(target_dir, exist_ok=True)
    scss_files = [f for f in os.listdir(source_dir) if f.endswith('.scss') and not f.startswith('_')]

    # ==============================================================================================
    # process scss files
    for scss_file in scss_files:
        temp_file = os.path.join(temp_dir, scss_file)
        shutil.copyfile(os.path.join(source_dir, scss_file), temp_file)

        with open(temp_file, 'r') as file:
            scss_content = file.read()

        if not scss_content.strip():
            continue

        import_statements = []
        lines = scss_content.split('\n')
        for line in lines:
            if line.startswith('@import'):
                import_statements.append(line)

        for import_statement in import_statements:
            imported_file = import_statement.split('"')[1]
            if not imported_file.startswith('_'):
                last_slash_index = max(imported_file.rfind('/'), imported_file.rfind('\\'))
                if last_slash_index != -1:
                    imported_file = imported_file[:last_slash_index + 1] + '_' + imported_file[last_slash_index + 1:]
                else:
                    imported_file = '_' + imported_file
            if not imported_file.endswith('.scss'):
                imported_file += '.scss'
            imported_file_path = os.path.join(source_dir, imported_file)
            with open(imported_file_path, 'r') as file:
                imported_content = file.read()
            scss_content = scss_content.replace(import_statement, imported_content)

        css_file = os.path.splitext(scss_file)[0] + '.css'
        css_path = os.path.join(target_dir, css_file)

        compiled_css = sass.compile(string=scss_content)

        # minify content
        if "-mini" in sys.argv or "-m" in sys.argv:
            compiled_css = compiled_css.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('  ', ' ')

        # write compiled css to target file
        with open(css_path, 'w') as file:
            file.seek(0)
            file.write(compiled_css)
            file.truncate()
