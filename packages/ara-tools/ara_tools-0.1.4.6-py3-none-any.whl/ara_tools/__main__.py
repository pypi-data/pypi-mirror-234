import os
import sys
import argparse
from .file_creator import FileCreator
from .filename_validator import is_valid_filename
from .classifier_validator import is_valid_classifier
from .template_manager import SpecificationBreakdownAspects

def cli():
    parser = argparse.ArgumentParser(description="Ara tools for creating files and directories.")
    parser.add_argument("action", help="Action to perform (e.g. 'create', 'delete', 'list')")
    parser.add_argument("filename", help="Filename for the file to be created or deleted", nargs="?")
    parser.add_argument("classifier", help="Classifier for the file to be created or deleted", nargs="?")
    parser.add_argument("aspect", help="Specification breakdown aspect", nargs="?")

    args = parser.parse_args()

    file_creator = FileCreator()

    if args.action.lower() == "create":
        # If all required parameters for SpecificationBreakdownAspects are provided
        if args.filename and args.classifier and args.aspect:
            sba = SpecificationBreakdownAspects()
            try:
                sba.create(args.filename, args.classifier, args.aspect)
            except ValueError as ve:
                print(f"Error: {ve}")
                sys.exit(1)
            return
        if not is_valid_filename(args.filename):
            print("Invalid filename provided. Please provide a valid filename.")
            sys.exit(1)

        if not is_valid_classifier(args.classifier):
            print("Invalid classifier provided. Please provide a valid classifier.")
            sys.exit(1)

        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        print(f"in __main__ file_creator.run called with {args.filename}, {args.classifier} and {template_path}")
        file_creator.run(args.filename, args.classifier, template_path)
    elif args.action.lower() == "delete":
        file_creator.delete(args.filename, args.classifier)
    elif args.action.lower() == "list":
        file_creator.list_files()
    else:
        print("Invalid action provided. Type ara -h for help")
        sys.exit(1)

if __name__ == "__main__":
    cli()
