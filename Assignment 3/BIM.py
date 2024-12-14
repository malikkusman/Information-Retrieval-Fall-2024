import os
import re

# Binary Independence Model

# Tokenizes the input text into words using a regex pattern.
def preprocess(text):
    
    tokens = re.findall(r'\b\w+\b', text.lower())
    #Removes common stop words (e.g., "and," "the") defined in a manual list.
    stop_words = {"and", "or", "but", "if", "while", "is", "at", "the", "a", "an", "in", "on", "of", "by", "to"}
    # Remove stop words and apply basic stemming by removing common suffixes
    tokens = [word.rstrip('ing').rstrip('ed').rstrip('s') for word in tokens if word not in stop_words]
    return tokens


def create_binary_vector(vocab, tokens):
    """
    Generates a binary vector for the vocabulary.
    """
    return [1 if term in tokens else 0 for term in vocab]

def jaccard_similarity(query_vec, doc_vec):
    """
    Calculates similarity between the query and document vectors.
    """
    intersection = sum(1 for q, d in zip(query_vec, doc_vec) if q == 1 and d == 1)
    union = sum(1 for q, d in zip(query_vec, doc_vec) if q == 1 or d == 1)
    return intersection / union if union > 0 else 0

def read_documents_from_folder(folder_path):
    """
    Read documents from a folder
    """
    documents = []
    doc_names = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                documents.append(file.read())
                doc_names.append(filename)
    return documents, doc_names

def binary_independence_model(query, folder_path, top_k=3):
    """
    Preprocesses both query and documents.
    Creates a unified vocabulary, binary vectors for query and documents, and computes similarity scores.
    sorts documents by similarity and returns the top k results.
    """
    documents, doc_names = read_documents_from_folder(folder_path)
    preprocessed_docs = [preprocess(doc) for doc in documents]
    preprocessed_query = preprocess(query)
    vocab = sorted(set(word for doc in preprocessed_docs for word in doc) | set(preprocessed_query))
    query_vec = create_binary_vector(vocab, preprocessed_query)
    doc_vectors = [create_binary_vector(vocab, doc) for doc in preprocessed_docs]
    scores = [jaccard_similarity(query_vec, doc_vec) for doc_vec in doc_vectors]
    ranked_docs = sorted(((idx, score) for idx, score in enumerate(scores) if score > 0), key=lambda x: x[1], reverse=True)
    return [{"document": doc_names[idx], "score": score} for idx, score in ranked_docs[:top_k]]


def main_bim():
    folder_path = "D:\\IR\\Information-Retrieval-Fall-2024\\Assignment 3\\douments"
    print(f"Using documents from folder: {folder_path}")
    while True:
        print("\n1. Binary Independence")
        print("2. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            query = input("Enter query: ")
            results = binary_independence_model(query, folder_path)
            for result in results:
                print(f"Document: {result['document']}, Score: {result['score']:.4f}")
        elif choice == "2":
            break

main_bim()
