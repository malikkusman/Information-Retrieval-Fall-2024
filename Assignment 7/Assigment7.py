from collections import Counter

def load_documents(file_path):
    """
    Reads a file containing document lines into a list.
    """
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return []


documents = load_documents('documents.txt')
"""
A predefined dictionary indicating the relevance of specific (query, document) pairs.
"""
relevance_judgments = {
    ("fox", 0): 1, 
    ("machine learning", 1): 1,  
    ("information retrieval", 2): 1, 
    ("fox", 3): 1  
}

# Simulated queries for demonstration
queries = ["fox", "dog", "cat", "fox", "fox", "dog"]

def compute_query_probabilities(queries):
    """ 
    Uses Counter to calculate the frequency of each query and normalizes it into probabilities.
    """
    total_queries = len(queries)
    if total_queries == 0:
        return {}
    query_freq = Counter(queries)
    return {query: freq / total_queries for query, freq in query_freq.items()}

def compute_document_probabilities(documents):
    """Compute uniform probabilities for all documents."""
    total_documents = len(documents)
    if total_documents == 0:
        return {}
    return {documents[i]: 1 / total_documents for i in range(total_documents)}

# Calculate query and document probabilities
query_probabilities = compute_query_probabilities(queries)
document_probabilities = compute_document_probabilities(documents)


def compute_relevance_probability(query, doc_name):
    """Compute the probability of relevance for a given query and document."""
    if (query, doc_name) in relevance_judgments:
        return relevance_judgments[(query, doc_name)]
    return 0.01  # Small probability for non-relevant pairs

def rank_documents_for_query(query):
    """Rank documents for a given query based on relevance probabilities."""
    scores = []
    for doc_name in documents:
        relevance_prob = compute_relevance_probability(query, doc_name)
        query_prob = query_probabilities.get(query, 0.01)
        doc_prob = document_probabilities.get(doc_name, 0.01)
        score = relevance_prob * query_prob * doc_prob
        scores.append((doc_name, score))
    return sorted(scores, key=lambda x: x[1], reverse=True)

# Example: Ranking documents for a query
query = "fox"
ranked_docs = rank_documents_for_query(query)
print(f"Ranked documents for query '{query}': {ranked_docs}")

# Part 2: Belief Network

# Define the Network Structure
belief_network = {
    "Query": ["Relevance"],
    "Relevance": ["Document"],
    "Document": []
}

# Calculate Joint and Marginal Probabilities

def joint_probability(query, doc_name):
    """Calculate the joint probability of query, relevance, and document."""
    relevance_prob = compute_relevance_probability(query, doc_name)
    doc_prob = document_probabilities.get(doc_name, 0.01)
    return relevance_prob * doc_prob

def marginal_probability(query):
    """Calculate the marginal probability of a query."""
    return sum(joint_probability(query, doc) for doc in documents)

# Implement Bayes' Theorem

def bayes_theorem(query, doc_name):
    """Calculate the probability of relevance given a query using Bayes' theorem."""
    joint_prob = joint_probability(query, doc_name)
    marginal_prob = marginal_probability(query)
    if marginal_prob == 0:
        return 0
    return joint_prob / marginal_prob

# Example: Compute probabilities for each document
belief_ranking = [(doc, bayes_theorem(query, doc)) for doc in documents]
belief_ranking = sorted(belief_ranking, key=lambda x: x[1], reverse=True)
print(f"Belief Network ranking for query '{query}': {belief_ranking}")
