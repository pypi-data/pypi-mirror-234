import os
from pathlib import Path
from .classifier import Classifier
from shutil import copy
from .directory_navigator import DirectoryNavigator

class TemplatePathManager:
    @staticmethod
    def get_template_base_path_aspects():
        """Returns the absolute path to the templates directory."""
        current_file_path = Path(__file__).absolute()  # Get current absolute path
        base_dir = current_file_path.parent  # Get directory of current file
        return base_dir / "templates" / "specification_breakdown_files"

    @staticmethod
    def get_template_base_path_artefacts():
        """Returns the absolute path to the templates directory."""
        current_file_path = Path(__file__).absolute()  # Get current absolute path
        base_dir = current_file_path.parent  # Get directory of current file
        return base_dir / "templates"

    def get_template_path(self, aspect):
        """Returns the path to the template for the given aspect."""
        base_path = self.get_template_base_path_aspects()
        return [
            (base_path / f"template.{aspect}.md", f"{aspect}.md"),
            (base_path / f"template.{aspect}_exploration.md", f"{aspect}_exploration.md")
        ]


class ArtefactFileManager:
    def __init__(self):
        self.template_manager = TemplatePathManager()

    def get_artefact_file_path(self, artefact_name, classifier, sub_directory=None):
        if not sub_directory:
            sub_directory = Classifier.get_sub_directory(classifier)
        return os.path.join(sub_directory, f"{artefact_name}.{classifier}")

    def get_data_directory_path(self, artefact_name, classifier, sub_directory=None):
        if not sub_directory:
            sub_directory = Classifier.get_sub_directory(classifier)
        return os.path.join(sub_directory, f"{artefact_name}.data")

    def get_data_directory(self, artefact_name):
        return f"{artefact_name}.data"

    def create_directory(self, artefact_file_path, data_dir):
        # make sure this function is called from the ara top level directory
        navigator = DirectoryNavigator()
        navigator.navigate_to_target()
        
        """Creates the data directory if needed and navigates into it."""
        if os.path.isfile(artefact_file_path):
            if not os.path.exists(data_dir):
                os.mkdir(data_dir)
            os.chdir(data_dir)
        else:
            raise ValueError(f"File {artefact_file_path} does not exist. Please create it first.")

    def copy_templates_to_directory(self, aspect):
        """Copies the templates for the given aspect to the current directory."""
        templates = self.template_manager.get_template_path(aspect)
        for src, dest in templates:
            if not src.exists():
                raise FileNotFoundError(f"Template file {src} does not exist.")
            copy(src, dest)


class SpecificationBreakdownAspects:
    VALID_ASPECTS = ['technology', 'concept', 'persona', 'customer']

    def __init__(self):
        self.file_manager = ArtefactFileManager()

    def validate_input(self, artefact_name, classifier, aspect):
        """Validates the inputs to ensure they're appropriate."""
        if not Classifier.is_valid_classifier(classifier):
            raise ValueError(f"{classifier} is not a valid classifier.")

        if aspect not in self.VALID_ASPECTS:
            raise ValueError(f"{aspect} does not exist. Please choose one of the {self.VALID_ASPECTS} list.")

    def create(self, artefact_name='artefact_name', classifier='classifier', aspect='specification_breakdown_aspect'):
        self.validate_input(artefact_name, classifier, aspect)
        artefact_file_path = self.file_manager.get_artefact_file_path(artefact_name, classifier)
        data_dir = self.file_manager.get_data_directory_path(artefact_name, classifier)
        self.file_manager.create_directory(artefact_file_path, data_dir)
        self.file_manager.copy_templates_to_directory(aspect)
