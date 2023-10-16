import os
import json

class ConfigLoader:
    def __init__(self, config_path='./ara/.araconfig'):
        self.config_path = config_path
        print("DEBUG: ConfigLoader initialized with path:", self.config_path)

    def load_config(self):
        print("DEBUG: Attempting to load config from:", self.config_path)
        try:
            with open(self.config_path, 'r') as f:
                data = json.load(f)
                print("DEBUG: Successfully loaded and parsed config.")
                return data
        except FileNotFoundError:
            print("DEBUG: FileNotFoundError raised.")
            raise ValueError("Failed to open the .araconfig file.")
        except json.JSONDecodeError:
            print("DEBUG: JSONDecodeError raised.")
            raise ValueError("Failed to parse the .araconfig file.")

class AraConfig:
    def __init__(self):
        self.paths = {}
        self.parameters = {}
        self.verified_paths = set()
        self.loader = ConfigLoader()
        print("DEBUG: AraConfig initialized.")

    def load_and_validate_config(self):
        print("DEBUG: Loading and validating config.")
        parsed_data = self.loader.load_config()
        self._store_paths(parsed_data)
        self._store_parameters(parsed_data)

    def _store_paths(self, parsed_data):
        print("DEBUG: Storing paths.")
        if "ARA_PATHS" not in parsed_data:
            print("DEBUG: 'ARA_PATHS' key missing in config.")
            raise ValueError("'ARA_PATHS' key missing in .araconfig.")
        self.paths = parsed_data["ARA_PATHS"]
        print("DEBUG: Paths stored:", self.paths)

    def _store_parameters(self, parsed_data):
        print("DEBUG: Storing parameters.")
        if "PARAMETERS" not in parsed_data:
            print("DEBUG: 'PARAMETERS' key missing in config.")
            raise ValueError("'PARAMETERS' key missing in .araconfig.")
        self.parameters = parsed_data["PARAMETERS"]
        print("DEBUG: Parameters stored:", self.parameters)

    def verify_paths(self, paths):
        print("DEBUG: Verifying paths.")
        
        if isinstance(paths, list):  # If input is a list, convert it to dictionary format
            paths = {"path_list": paths}

        for path_type, path_list in paths.items():
            for path in path_list:
                if path in self.verified_paths:
                    print(f"DEBUG: Path '{path}' already verified. Skipping.")
                    continue
                if not os.path.exists(path):
                    print(f"DEBUG: Path '{path}' does not exist.")
                    raise ValueError(f"The path {path} does not exist.")
                print(f"DEBUG: Path '{path}' verified successfully.")
                self.verified_paths.add(path)


    def get_path(self, path_key):
        print(f"DEBUG: Getting path for key: {path_key}")
        if not self.paths:
            print("DEBUG: Paths empty. Reloading config.")
            self.load_and_validate_config()
        return self.paths.get(path_key, None)

    def get_parameter(self, parameter_key):
        print(f"DEBUG: Getting parameter for key: {parameter_key}")
        if not self.parameters:
            print("DEBUG: Parameters empty. Reloading config.")
            self.load_and_validate_config()
        return self.parameters.get(parameter_key, None)
