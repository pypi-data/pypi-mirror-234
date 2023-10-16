import os
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import pyglossary

class ConfigManager:
    def __init__(self, root_dir):
        self.root_dir = root_dir

    def validate_config_file(self):
        return os.path.exists(os.path.join(self.root_dir, '.araconfig'))

    def get_ara_paths(self):
        # For simplification, we're assuming that the .araconfig file contains paths line by line.
        with open(os.path.join(self.root_dir, '.araconfig'), 'r') as file:
            paths = file.readlines()
        return [path.strip() for path in paths if 'glossary_dir' not in path]

class DirectoryCrawler:
    def crawl_through_directories(self, paths):
        files_list = []
        for path in paths:
            for root, _, files in os.walk(path):
                for file in files:
                    files_list.append(os.path.join(root, file))
        return files_list

class TermExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def extract_terms_from_files(self, files):
        terms_list = []
        for file in files:
            with open(file, 'r') as f:
                text = f.read()
                terms_list.extend(self._extract_from_text(text))
        return terms_list

    def _extract_from_text(self, text):
        doc = self.nlp(text)
        tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
        
        vectorizer = TfidfVectorizer(ngram_range=(1,3))
        tfidf_matrix = vectorizer.fit_transform([" ".join(tokens)])
        feature_names = vectorizer.get_feature_names_out()
        tfidf_sorting = tfidf_matrix.sum(axis=0).argsort()[0, ::-1]
    
        top_terms = [feature_names[i] for i in tfidf_sorting[0:10]]
        terms_in_context = [next(sent for sent in text.split('.') if term in sent) for term in top_terms]
        
        return terms_in_context

class GlossaryManager:
    def save_glossary(self, terms):
        glossary = pyglossary.Glossary()
        for term in terms:
            glossary.add_term(term, "example_definition")  # This should be expanded for real definitions
        glossary.save(os.path.join("glossary_dir", "ara_glossary.md"))
        return True

class GlossaryGenerator:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.config_manager = ConfigManager(root_dir)
        self.crawler = DirectoryCrawler()
        self.extractor = TermExtractor()
        self.glossary_manager = GlossaryManager()

    def validate_config_file(self):
        return self.config_manager.validate_config_file()

    def get_ara_paths(self):
        return self.config_manager.get_ara_paths()

    def crawl_through_directories(self, paths):
        return self.crawler.crawl_through_directories(paths)

    def extract_terms_from_files(self, files):
        return self.extractor.extract_terms_from_files(files)

    def save_glossary(self, terms):
        return self.glossary_manager.save_glossary(terms)

    def update_with_new_terms(self):
        # This should be expanded with the logic to check for new terms and update the existing glossary
        return True

    def handle_duplicate_terms(self):
        # This should be expanded with the logic to handle duplicate terms, for now, returning a dummy value
        return True

# Additional methods and functionalities based on the feature file can be added to GlossaryGenerator.
