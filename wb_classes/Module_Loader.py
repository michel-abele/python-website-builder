import os
import importlib.util

class Module_Loader:
    def __init__(self, modules_path):
        self.modules_path = modules_path

    # ==============================================================================================
    # load modules
    def load_modules(self, module_names):
        for module_name in module_names:
            try:
                self._import_module(module_name)
            except (ImportError, FileNotFoundError) as e:
                print(e)
                continue

    # ==============================================================================================
    # helper methods
            
    # import module
    def _import_module(self, module_name):
        module_path = os.path.join(self.modules_path, f"{module_name}.py")
        if os.path.exists(module_path):
            try:
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
            except ImportError as e:
                raise ImportError(f"Error: {e}")
        else:
            raise FileNotFoundError(f"Error: The module '{module_name}' does not exist!")
