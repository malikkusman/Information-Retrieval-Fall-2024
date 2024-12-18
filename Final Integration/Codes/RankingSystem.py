import os
import math
from collections import Counter

class RankingSystem:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.documents = self.load_documents()
        if not self.documents:
            raise ValueError("No valid documents found in the specified folder.")
    
    def load_documents(self):
        """Load text documents from the specified folder."""
        documents = {}
        for file_name in os.listdir(self.folder_path):
            if file_name.endswith('.txt'):
                with open(os.path.join(self.folder_path, file_name), 'r', encoding='utf-8') as f:
                    doc = f.read().split("\n", 1)
                    title = doc[0].replace("Title: ", "")
                    content = doc[1].replace("Content: ", "")
                    documents[file_name] = content
        return documents

    def tokenize(self, text):
        """Convert text into lowercase words, removing special characters and stop words."""
        stop_words = {
            "and", "the", "is", "in", "at", "of", "on", "a", "to", "it", "for", 
            "with", "as", "was", "by", "an", "be", "that", "this", "or", "are", "from", "but"
        }
        return [word.lower() for word in text.split() if word.isalnum() and word.lower() not in stop_words]

    # --- Ranking Methods ---
    def rank_by_keyword_matching(self, query):
        """Rank documents based on keyword matching."""
        query_tokens = self.tokenize(query)
        rankings = []
        for doc_name, content in self.documents.items():
            doc_tokens = self.tokenize(content)
            matches = sum(1 for word in query_tokens if word in doc_tokens)
            rankings.append((doc_name, matches))
        return sorted(rankings, key=lambda x: x[1], reverse=True)

    def calculate_tf(self, doc):
        """Calculate term frequency for a document."""
        words = self.tokenize(doc)
        total_terms = len(words)
        tf = Counter(words)
        return {term: freq / total_terms for term, freq in tf.items()}

    def calculate_idf(self):
        """Calculate inverse document frequency for all terms."""
        num_docs = len(self.documents)
        idf = {}
        all_words = set()
        
        # Collect all unique words from all documents
        for content in self.documents.values():
            all_words.update(self.tokenize(content))
        
        # Calculate IDF for each word
        for word in all_words:
            doc_count = sum(1 for content in self.documents.values() if word in self.tokenize(content))
            idf[word] = math.log(num_docs / (1 + doc_count))  # Avoid division by zero
        return idf

    def calculate_tfidf(self, doc, idf):
        """Calculate TF-IDF scores for a document."""
        tf = self.calculate_tf(doc)
        return {term: tf[term] * idf[term] for term in tf if term in idf}

    def rank_by_tfidf(self, query):
        """Rank documents based on TF-IDF scores."""
        idf = self.calculate_idf()
        query_vector = self.calculate_tfidf(query, idf)
        doc_vectors = {doc_name: self.calculate_tfidf(content, idf) for doc_name, content in self.documents.items()}
        
        rankings = []
        for doc_name, vector in doc_vectors.items():
            score = sum(query_vector.get(term, 0) for term in vector)
            rankings.append((doc_name, score))
        return sorted(rankings, key=lambda x: x[1], reverse=True)

    def cosine_similarity(self, vec1, vec2):
        """Calculate cosine similarity between two vectors."""
        dot_product = sum(vec1[term] * vec2.get(term, 0) for term in vec1)
        magnitude1 = math.sqrt(sum(val ** 2 for val in vec1.values()))
        magnitude2 = math.sqrt(sum(val ** 2 for val in vec2.values()))
        if magnitude1 == 0 or magnitude2 == 0:
            return 0
        return dot_product / (magnitude1 * magnitude2)

    def rank_by_cosine_similarity(self, query):
        """Rank documents based on cosine similarity to the query."""
        idf = self.calculate_idf()
        query_vector = self.calculate_tfidf(query, idf)
        doc_vectors = {doc_name: self.calculate_tfidf(content, idf) for doc_name, content in self.documents.items()}
        
        rankings = []
        for doc_name, vector in doc_vectors.items():
            similarity = self.cosine_similarity(query_vector, vector)
            rankings.append((doc_name, similarity))
        return sorted(rankings, key=lambda x: x[1], reverse=True)

