import re
import os

# NON OVERLAPPED MODEL

def preprocess(text):
    """
    Tokenizes and lowercases text.
    """
    tokens = re.findall(r'\b\w+\b', text.lower())
    stop_words = {"and", "or", "but", "if", "while", "is", "at", "the", "a", "an", "in", "on", "of", "by", "to"}
    return [word for word in tokens if word not in stop_words]

def read_documents_from_folder(folder_path):
    """READ DOCUMENT FROM THE FOLDER"""
    documents = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                documents[filename] = file.read()
    return documents

def retrieve_documents_by_term(term, documents):
    """
    For each query term, checks if it exists in the preprocessed content of any document.
    """
    relevant_docs = set()
    for doc_name, content in documents.items():
        preprocessed_content = preprocess(content)
        if term in preprocessed_content:
            relevant_docs.add(doc_name)
    return relevant_docs

def non_overlapped_list_model(terms, folder_path):
    """
    Combines all sets of documents for the terms into a single sET.
    """
    documents = read_documents_from_folder(folder_path)
    combined_docs = set()
    for term in terms:
        preprocessed_term = preprocess(term)[0]
        combined_docs |= retrieve_documents_by_term(preprocessed_term, documents)
    return list(combined_docs)


def main_non_overlapped():
    folder_path = "D:\\IR\\Information-Retrieval-Fall-2024\\Assignment 3\\douments"
    print(f"Using folder: {folder_path}")
    while True:
        print("\n1 Non Overlappped Model")
        print("2. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            terms = input("Enter comma-separated terms: ").split(",")
            results = non_overlapped_list_model(terms, folder_path)
            print("\nResults:")
            for doc in results:
                print(doc)
        elif choice == "2":
            break

main_non_overlapped()
