# Interference Model

from flask import Flask, request, jsonify, render_template
from collections import Counter

def load_documents(file_path):
    """
    Load documents from a text file, each line is a document.
    """
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip()]  # Strip whitespace and filter empty lines


document_file = 'documents.txt'  # Path to the document file
documents = load_documents(document_file)

# These are sample queries and their corresponding relevance judgments for testing purposes.
queries = ["quick fox", "lazy dog", "fast fox"]
relevance_judgments = {
    "quick fox": ["The quick brown fox jumps over the lazy dog", 
                  "The quick brown fox is very quick and fast"],
    "lazy dog": ["The lazy dog sleeps all day long", 
                 "The quick brown fox jumps over the lazy dog"],
    "fast fox": ["The quick brown fox is very quick and fast", 
                 "A fast fox is better than a lazy dog"],
}

def tokenize(text):
    """
    Split text into lowercase tokens (words).
    """
    return text.lower().split()

def compute_term_frequencies(documents):
    """
    Compute term frequencies for all documents.
    """
    tf = []
    for doc in documents:
        term_counts = Counter(tokenize(doc))  # Count occurrences of each term in the document
        tf.append(term_counts)
    return tf

def compute_probabilities(query, document, tf, vocab_size):
    """
    Compute P(Query | Document) using term frequencies with add-one smoothing.
    """
    query_terms = tokenize(query) 
    doc_terms = tokenize(document) 
    doc_length = len(doc_terms)  

    prob = 1.0  # Initialize probability
    for term in query_terms:
        term_freq = tf[documents.index(document)].get(term, 0)  # Term frequency in the document
        prob *= (term_freq + 1) / (doc_length + vocab_size)  # Add-one smoothing to avoid zero probabilities
    return prob


def rank_documents(query, documents, tf):
    """
    Rank documents based on relevance probability for a given query.
    """
    # Build the vocabulary from all documents
    vocab = set(token for doc in documents for token in tokenize(doc))
    vocab_size = len(vocab)  # Number of unique terms

    # Compute scores for each document
    scores = {}
    for doc in documents:
        scores[doc] = compute_probabilities(query, doc, tf, vocab_size)

    # Sort documents by their scores in descending order
    ranked_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked_docs

# Precompute Term Frequencies for Documents
tf = compute_term_frequencies(documents)


app = Flask(__name__)

@app.route("/")
def index():
    """
    Render the home page with a list of sample queries.
    """
    return render_template("index.html", queries=queries)

@app.route("/rank", methods=["POST"])
def rank():
    """
    Rank documents for a given query and return the result as JSON.
    """
    query = request.form.get("query")
    ranked_docs = rank_documents(query, documents, tf) 
    return jsonify({"query": query, "ranked_docs": ranked_docs})

# Main Entry Point
if __name__ == "__main__":
    app.run(debug=True)
