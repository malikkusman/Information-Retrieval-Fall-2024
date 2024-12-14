import os
import re

# PROXIMAL NODE MODEL

def preprocess_document(doc_content):
    """
    Tokenizes and lowercases text.
    """
    words = re.findall(r'\b\w+\b', doc_content.lower())
    stop_words = {"and", "or", "but", "if", "while", "is", "at", "the", "a", "an", "in", "on", "of", "by", "to"}
    return [word for word in words if word not in stop_words]

def build_document_graph(words):
    """
    Treats words as nodes and connects adjacent words with edges to create a document graph.
    """
    graph = {}
    for i in range(len(words) - 1):
        word1, word2 = words[i], words[i + 1]
        graph.setdefault(word1, set()).add(word2)
        graph.setdefault(word2, set()).add(word1)
    return graph

def is_relevant_document(graph, proximal_nodes):
    """
    Checks if any user-defined "proximal nodes" (query words) exist in the document graph.
    If a proximal node is found, the document is considered relevant.
    """
    return any(node in graph for node in proximal_nodes)

def read_documents_from_folder(folder_path):
    """read documents from the folder"""
    documents = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                documents[filename] = file.read()
    return documents

def proximal_nodes_model():
    folder_path = "D:\\IR\\Information-Retrieval-Fall-2024\\Assignment 3\\douments"
    while True:
        print("\n1. Proximal Node Model")
        print("2. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            proximal_nodes = input("Enter nodes (comma-separated): ").lower().split(",")
            proximal_nodes = [node.strip() for node in proximal_nodes]
            documents = read_documents_from_folder(folder_path)
            relevant_docs = []
            for filename, content in documents.items():
                words = preprocess_document(content)
                doc_graph = build_document_graph(words)
                if is_relevant_document(doc_graph, proximal_nodes):
                    relevant_docs.append(filename)
            print("\nRelevant Documents:")
            for doc in relevant_docs:
                print(doc)
        elif choice == "2":
            break

proximal_nodes_model()
