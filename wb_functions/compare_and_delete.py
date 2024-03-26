import os

def compare_and_delete(source, target, exclude_dir=None):
    for item in os.listdir(target):
        target_item = os.path.join(target, item)
        if os.path.isfile(target_item) and item not in os.listdir(source):
            os.remove(target_item)
        elif os.path.isdir(target_item) and item != exclude_dir:
            compare_and_delete(os.path.join(source, item), target_item, exclude_dir)

    for root, dirs, files in os.walk(target, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
