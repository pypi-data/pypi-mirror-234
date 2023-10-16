import os

class DirectorySearcher:

    @staticmethod
    def find_directory(target_directory, start_directory):
        print(f"Searching for '{target_directory}' starting from '{start_directory}'...")

        # Check if the current directory is the target directory
        if os.path.basename(start_directory) == target_directory:
            print(f"Found the target directory: {start_directory}")
            return start_directory

        # Search strategy 1: Start from the current directory and look upwards
        print("Trying search upwards strategy...")
        found_directory = DirectorySearcher._search_upwards(target_directory, start_directory)
        if found_directory:
            print(f"Found using search upwards strategy: {found_directory}")
            return found_directory

        # Search strategy 2: Start from the current directory and look downwards
        print("Trying search downwards strategy...")
        found_directory = DirectorySearcher._search_downwards(target_directory, start_directory)
        if found_directory:
            print(f"Found using search downwards strategy: {found_directory}")
            return found_directory

        # Search strategy 3: Look in parallel directories at the same level and then move upwards
        print("Trying search parallel strategy...")
        current_directory = start_directory
        while current_directory != os.path.dirname(current_directory):  # Ensure loop breaks at root
            found_directory = DirectorySearcher._search_parallel(target_directory, current_directory)
            if found_directory:
                print(f"Found using search parallel strategy: {found_directory}")
                return found_directory
            current_directory = os.path.dirname(current_directory)

        print("Target directory not found.")
        return None

    @staticmethod
    def _search_upwards(target_directory, start_directory):
        current_directory = start_directory
        print(f"Initial directory for upwards search: {current_directory}")
        while current_directory != os.path.dirname(current_directory):  # Ensure loop breaks at root
            current_directory = os.path.dirname(current_directory)  # Move up to parent directory first
            print(f"Checking parent directory: {current_directory}")
            if os.path.basename(current_directory) == target_directory:
                print(f"Found target '{target_directory}' in parent directory: {current_directory}")
                return current_directory
            potential_path = os.path.join(current_directory, target_directory)
            if os.path.exists(potential_path) and os.path.isdir(potential_path):
                print(f"Found target '{target_directory}' at potential path: {potential_path}")
                return potential_path
        print(f"Target '{target_directory}' not found using upwards search.")
        return None

    @staticmethod
    def _search_downwards(target_directory, start_directory):
        print(f"Starting downwards search from: {start_directory}")
        for root, dirs, _ in os.walk(start_directory):
            if target_directory in dirs:
                print(f"Found target '{target_directory}' in directory: {root}")
                return os.path.join(root, target_directory)
        print(f"Target '{target_directory}' not found using downwards search.")
        return None

    @staticmethod
    def _search_parallel(target_directory, start_directory):
        parent_directory = os.path.dirname(start_directory)
        
        # Get the sibling directories
        sibling_dirs = [os.path.join(parent_directory, d) for d in os.listdir(parent_directory) 
                    if d != os.path.basename(start_directory)]

        
        print(f"Siblings of '{start_directory}': {sibling_dirs}")
        
        # Check if one of the siblings is the target directory
        for sibling in sibling_dirs:
            if os.path.basename(sibling) == target_directory:
                print(f"Found target '{target_directory}' directly in sibling directory: {sibling}")
                return sibling
        
        # Search downwards in each sibling directory for the target
        for sibling in sibling_dirs:
            print(f"Searching for target '{target_directory}' downwards from sibling directory: {sibling}")
            potential_path = DirectorySearcher._search_downwards(target_directory, sibling)
            if potential_path:
                print(f"Found target '{target_directory}' in a subdirectory of sibling: {sibling}")
                return potential_path
        
        print(f"Target '{target_directory}' not found in siblings or their sub-directories.")
        return None

