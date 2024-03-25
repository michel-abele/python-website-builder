import os

def check_multilingual_website(source_path):
    is_multilingual_website = True
    
    # ==============================================================================================
    # check for multilingual website
    subdirectories = os.listdir(source_path)
    for subdir in subdirectories:
        if len(subdir) == 2 and subdir.isalpha():
            continue
        elif len(subdir) == 5 and subdir[:2].isalpha() and subdir[2] == '-' and subdir[3:].isalpha():
            continue
        else:
            is_multilingual_website = False

    # ==============================================================================================
    # create sitemap.json files
    if is_multilingual_website:
        sitemap_dir = os.path.join("./temp", "sitemap")
        os.makedirs(sitemap_dir, exist_ok=True)

        # save a JSON file for each language directory
        for subdir in subdirectories:
            if len(subdir) == 2 and subdir.isalpha():
                json_file = os.path.join(sitemap_dir, f"{subdir}.json")
                with open(json_file, "w") as f:
                    f.write("{}")
            elif len(subdir) == 5 and subdir[:2].isalpha() and subdir[2] == '-' and subdir[3:].isalpha():
                json_file = os.path.join(sitemap_dir, f"{subdir}.json")
                with open(json_file, "w") as f:
                    f.write("{}")
    else:
        json_file = os.path.join("./temp", f"sitemap.json")
        with open(json_file, "w") as f:
            f.write("{}")

    # ==============================================================================================
    return is_multilingual_website
