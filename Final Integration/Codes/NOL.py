import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import defaultdict

class NonOverlappedListModel:
    def __init__(self, docs_folder):
        self.docs_folder = docs_folder
        self.documents = {}
        self.preprocessed_docs = {}
        self.term_doc_map = defaultdict(set)
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()

    def preprocess_text(self, text):
        """Preprocess text by tokenizing, removing stop words, and stemming."""
        tokens = word_tokenize(text.lower())
        filtered_tokens = [self.stemmer.stem(word) for word in tokens if word.isalnum() and word not in self.stop_words]
        return filtered_tokens

    def load_document(self, filename):
        """Load and preprocess a single document."""
        file_path = os.path.join(self.docs_folder, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            preprocessed_terms = self.preprocess_text(content)
            return content, preprocessed_terms

    def build_term_document_map(self):
        """Create a mapping of terms to the documents they appear in."""
        for filename in os.listdir(self.docs_folder):
            if filename.endswith(".txt"):
                content, preprocessed_terms = self.load_document(filename)
                self.documents[filename] = content
                self.preprocessed_docs[filename] = preprocessed_terms
                for term in preprocessed_terms:
                    self.term_doc_map[term].add(filename)

    def retrieve_documents_for_term(self, term):
        """Retrieve documents containing the specified term."""
        # Preprocess the input term to handle multiple words
        stemmed_terms = self.preprocess_text(term)
        
        # Collect documents for all stemmed terms (union of all term's document lists)
        docs = set()
        for stemmed_term in stemmed_terms:
            docs.update(self.term_doc_map.get(stemmed_term, set()))
        
        return docs

    def retrieve_non_overlapping_documents(self, terms):
        """Retrieve a non-overlapping set of documents for multiple terms."""
        non_overlapping_docs = set()  # Use a set to avoid duplicate documents

        for term in terms:
            term_docs = self.retrieve_documents_for_term(term)  # Get documents for the term
            non_overlapping_docs.update(term_docs)  # Union of document sets

        return non_overlapping_docs

