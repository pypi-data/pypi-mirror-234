import os
from .classifier import Classifier
from .template_manager import DirectoryNavigator
from pathlib import Path
import shutil
from shutil import rmtree
from shutil import copyfile

class FileCreator:
        
    def __init__(self, file_system=None):
        self.file_system = file_system or os

    def create_artefact_exploration(self, dir_path, template_path, classifier):
        # print(f"[DEBUG] dir_path: {dir_path}")
        # print(f"[DEBUG] template_path: {template_path}")
        # print(f"[DEBUG] classifier: {classifier}")

        if not template_path:
            raise ValueError("template_path must not be None or empty!")

        if not classifier:
            raise ValueError("classifier must not be None or empty!")

        # Standard exploration artefact
        self._copy_template_file(dir_path, template_path, f"template.{classifier}_exploration.md", f"{classifier}_exploration.md")

        # Additional exploration artefact for 'feature' classifier
        if classifier == 'feature':
            self._copy_template_file(dir_path, template_path, "template.steps_exploration.md", "steps_exploration.md")

    def _copy_template_file(self, dir_path, template_path, source_name, dest_name):
        source = Path(template_path) / source_name
        destination = Path(dir_path) / dest_name

        # print(f"[DEBUG] Constructed destination path: {destination}")
        # print(f"[DEBUG] Constructed source path: {source}")

        if not source.exists():
            print("[ERROR] Source file does not exist!")
            raise FileNotFoundError(f"Source file {source} not found!")
        
        if not destination.parent.exists():
            print("[ERROR] Destination directory does not exist!")
            raise NotADirectoryError(f"Destination directory {destination.parent} does not exist!")

        # print(f"[DEBUG] Copying file from {source} to {destination}...")
        copyfile(source, destination)
        print("[DEBUG] Copy completed.")


    def create_file(self, file_path, template_path=None, classifier=None, filename=None):
        if template_path and classifier:
            template_file_path = self.file_system.path.join(template_path, f"template.{classifier}")
            if self.file_system.path.exists(template_file_path):
                with open(template_file_path, "r") as template_file:
                    template_content = template_file.read()

                template_content = template_content.replace("<descriptive title>", filename.replace("-", " "))

                with open(file_path, "w") as file:
                    file.write(template_content)
            else:
                with open(file_path, "w") as file:
                    pass
        else:
            with open(file_path, "w") as file:
                pass

    def create_directory(self, dir_path):
        self.file_system.makedirs(dir_path, exist_ok=True)

    def template_exists(self, template_path, template_name):
        if not template_path:
            return False

        full_path = self.file_system.path.join(template_path, template_name)

        if not self.file_system.path.isfile(full_path):
            print(f"Template file '{template_name}' not found at: {full_path}")
            return False

        return True


    def run(self, filename, classifier, template_path=None):
        # make sure this function is always called from the ara top level directory
        navigator = DirectoryNavigator()
        navigator.navigate_to_target()

        if not Classifier.is_valid_classifier(classifier):
            print("Invalid classifier provided. Please provide a valid classifier.")
            return

        sub_directory = Classifier.get_sub_directory(classifier)
        self.file_system.makedirs(sub_directory, exist_ok=True)

        file_path = self.file_system.path.join(sub_directory, f"{filename}.{classifier}")
        dir_path = self.file_system.path.join(sub_directory, f"{filename}.data")

        if self.file_system.path.exists(file_path) or self.file_system.path.exists(dir_path):
            user_choice = input("File or directory already exists. Do you want to overwrite the existing file and directory? (Y/N): ")

            if user_choice.lower() != "y":
                print("No changes were made to the existing file and directory.")
                return

        template_name = f"template.{classifier}"
        if template_path and not self.template_exists(template_path, template_name):
            print(f"Template file '{template_name}' not found in the specified template path.")
            return

        

        self.create_file(file_path, template_path, classifier, filename)
        self.create_directory(dir_path)
        self.create_artefact_exploration(dir_path, template_path, classifier)

        print(f"Created file: {file_path}")
        print(f"Created directory: {dir_path}")
        print(f"Created artefact exploration: {dir_path}/{classifier}_exploration.md")

    def delete(self, filename, classifier):
        print(f"DEBUG: Starting delete function...")  # DEBUG PRINT
        
        # make sure this function is always called from the ara top level directory
        navigator = DirectoryNavigator()
        navigator.navigate_to_target()

        if not Classifier.is_valid_classifier(classifier):
            print("Invalid classifier provided. Please provide a valid classifier.")
            return

        sub_directory = Classifier.get_sub_directory(classifier)
        print(f"DEBUG: Subdirectory determined: {sub_directory}")  # DEBUG PRINT

        file_path = self.file_system.path.join(sub_directory, f"{filename}.{classifier}")
        dir_path = self.file_system.path.join(sub_directory, f"{filename}.data")

        print(f"DEBUG: File path to delete: {file_path}")  # DEBUG PRINT
        print(f"DEBUG: Directory path to delete: {dir_path}")  # DEBUG PRINT

        if not self.file_system.path.exists(file_path) or not self.file_system.path.exists(dir_path):
            print("File or directory not found.")
            return

        user_choice = input("Are you sure you want to delete the file and directory? (Y/N): ")

        if user_choice.lower() != "y":
            print("No changes were made.")
            return

        print(f"DEBUG: Proceeding to delete...")  # DEBUG PRINT

        self.file_system.remove(file_path)
        shutil.rmtree(dir_path)

        print(f"Deleted file: {file_path}")
        print(f"Deleted directory: {dir_path}")

        print(f"DEBUG: Deletion completed.")  # DEBUG PRINT

    def list_files(self):
        # make sure this function is always called from the ara top level directory
        navigator = DirectoryNavigator()
        navigator.navigate_to_target()

        files_by_classifier = {classifier: [] for classifier in Classifier.ordered_classifiers()}

        for root, dirs, files in self.file_system.walk("."):
            for file in files:
                for classifier in Classifier.ordered_classifiers():
                    if file.endswith(f".{classifier}"):
                        files_by_classifier[classifier].append(self.file_system.path.join(root, file))

        for classifier in Classifier.ordered_classifiers():
            if files_by_classifier[classifier]:
                print(f"{classifier.capitalize()} files:")
                for file in files_by_classifier[classifier]:
                    print(f"  - {file}")
                print()