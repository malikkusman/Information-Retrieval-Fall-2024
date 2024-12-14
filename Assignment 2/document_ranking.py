
import math
from collections import Counter

# Step 2: Gather Your Documents
def load_documents():
    """Loads text files from a static list of file names."""
    folder_path = "D:\\IR\\Information-Retrieval-Fall-2024\\Assignment 2\\documents\\"
    file_names = ["doc1.txt", "doc2.txt", "doc3.txt", "doc4.txt", "doc5.txt"]

    documents = {}
    for file_name in file_names:
        try:
            with open(folder_path + file_name, 'r', encoding='utf-8') as file:
                documents[file_name] = file.read()
        except FileNotFoundError:
            print(f"File {file_name} not found!")
    return documents

# Step 4: Implement Keyword Matching
def keyword_match(query, documents):
    """Ranks documents based on keyword matching."""
    query_keywords = query.lower().split()
    doc_scores = {}
    for doc_name, content in documents.items():
        content_keywords = content.lower().split()
        match_count = sum(1 for word in query_keywords if word in content_keywords)
        doc_scores[doc_name] = match_count
    ranked_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
    return ranked_docs

# Step 5: Implement Manual TF-IDF Scoring
def compute_tf(doc):
    """Calculates Term Frequency (TF) for a document."""
    words = doc.lower().split()
    word_count = Counter(words)
    total_words = len(words)
    return {word: count / total_words for word, count in word_count.items()}

def compute_idf(documents):
    """Calculates Inverse Document Frequency (IDF) for the corpus."""
    num_documents = len(documents)
    word_document_count = Counter()
    
    for doc in documents.values():
        unique_words = set(doc.lower().split())
        for word in unique_words:
            word_document_count[word] += 1
    
    return {word: math.log(num_documents / (count + 1)) for word, count in word_document_count.items()}

def compute_tfidf(doc, tf, idf):
    """Calculates TF-IDF for a document."""
    return {word: tf[word] * idf.get(word, 0) for word in tf}

def cosine_similarity(vec1, vec2):
    """Calculates cosine similarity between two vectors."""
    dot_product = sum(vec1.get(word, 0) * vec2.get(word, 0) for word in vec1)
    norm1 = math.sqrt(sum(val**2 for val in vec1.values()))
    norm2 = math.sqrt(sum(val**2 for val in vec2.values()))
    if norm1 == 0 or norm2 == 0:
        return 0
    return dot_product / (norm1 * norm2)

def tfidf_rank(query, documents):
    """Ranks documents using manual TF-IDF scoring."""
    tfidf_vectors = {}
    # Compute TF for each document
    tf_values = {doc_name: compute_tf(content) for doc_name, content in documents.items()}
    
    # Compute IDF for the whole corpus
    idf_values = compute_idf(documents)
    
    # Compute TF-IDF for each document
    for doc_name in documents:
        tfidf_vectors[doc_name] = compute_tfidf(documents[doc_name], tf_values[doc_name], idf_values)
    
    # Compute TF-IDF for the query
    query_tf = compute_tf(query)
    query_tfidf = compute_tfidf(query, query_tf, idf_values)
    
    # Compute cosine similarity between query TF-IDF and document TF-IDF
    doc_scores = {}
    for doc_name, doc_tfidf in tfidf_vectors.items():
        score = cosine_similarity(query_tfidf, doc_tfidf)
        doc_scores[doc_name] = score
    
    ranked_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
    return ranked_docs

# Step 6: Display the Ranked Documents
def display_ranked_docs(ranked_docs, documents, top_n=5):
    """Displays the top N ranked documents."""
    print("\nTop Relevant Documents:")
    for i, (doc_name, score) in enumerate(ranked_docs[:top_n]):
        print(f"{i+1}. {doc_name} (Score: {score:.2f})")
        print(f"   Snippet: {documents[doc_name][:100]}...\n")

# Step 7: User Interaction
def main():
    print("Welcome to the Document Ranking System")
    
    # Load documents using the static file path
    documents = load_documents()
    if not documents:
        print("No text documents found in the specified folder!")
        return
    
    while True:
        print("\nOptions:")
        print("1. Rank documents using keyword matching")
        print("2. Rank documents using TF-IDF")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ").strip()
        
        if choice == '3':
            print("Exiting the system. Goodbye!")
            break
        
        query = input("Enter your query: ").strip()
        if not query:
            print("Query cannot be empty. Please try again.")
            continue
        
        if choice == '1':
            ranked_docs = keyword_match(query, documents)
        elif choice == '2':
            ranked_docs = tfidf_rank(query, documents)
        else:
            print("Invalid choice. Please select again.")
            continue
        
        display_ranked_docs(ranked_docs, documents)

# Run the main function
if __name__ == "__main__":
    main()
