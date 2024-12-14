import numpy as np
import nltk
from nltk.corpus import wordnet
import os

# Download required NLTK data for tokenization
nltk.download('punkt_tab')


def preprocess_text(query):
    """ 
    Converts the query to lowercase and tokenizes it into words.
    """
    words = nltk.word_tokenize(query.lower())
    return words

def identify_keywords(words):
    """
    Filters out non-alphabetic words to retain important keywords.
    """
    important_keywords = [word for word in words if word.isalpha()]
    return important_keywords

def get_synonyms(word):
    """
    Uses WordNet to find synonyms for each keyword, enhancing query coverage.
    """
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)

def expand_query(keywords):
    """Combines keywords and their synonyms into an expanded list."""
    expanded_query = []
    for word in keywords:
        expanded_query.append(word)
        synonyms = get_synonyms(word)
        expanded_query.extend(synonyms)
    return expanded_query

# Retrieve relevant documents by matching expanded query terms with the text content in files
def retrieve_documents(expanded_query, folder_path):
    relevant_documents = []
    for filename in os.listdir(folder_path):  # Iterate over all files in the folder
        if filename.endswith('.txt'):  # Process only text files
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                doc_text = file.read().lower()
                # Check if any expanded query term is in the document
                for term in expanded_query:
                    if term in doc_text:
                        relevant_documents.append((filename, doc_text[:200]))  # Include filename and snippet
                        break  # Avoid duplicating the same document
    return relevant_documents

# Generate random relevance scores for retrieved documents
def calculate_relevance_score(relevant_docs):
    num_docs = len(relevant_docs)
    X = np.random.rand(num_docs, 10)  # Random features matrix for demonstration
    return X

# Activation function for neural network layers
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Derivative of sigmoid function for backpropagation
def sigmoid_derivative(x):
    return x * (1 - x)


def train_neural_network(X, y, epochs, learning_rate):
    # The model starts with random weights and biases.
    input_size = X.shape[1]
    hidden_size = 8
    output_size = 1

    # Initialize weights and biases for input-to-hidden and hidden-to-output layers
    W_input = np.random.randn(input_size, hidden_size) * 0.1
    B_input = np.zeros((1, hidden_size))
    W_output = np.random.randn(hidden_size, output_size) * 0.1
    B_output = np.zeros((1, output_size))

    # In each epoch, it makes predictions on the entire dataset.
    for epoch in range(epochs):
        # Forward pass
        hidden_layer_input = np.dot(X, W_input) + B_input
        hidden_layer_output = sigmoid(hidden_layer_input)
        output_layer_input = np.dot(hidden_layer_output, W_output) + B_output
        output = sigmoid(output_layer_input)

        # After each prediction, the error (loss) is compute
        output_error = y - output
        output_delta = output_error * sigmoid_derivative(output)
        hidden_error = np.dot(output_delta, W_output.T)
        hidden_delta = hidden_error * sigmoid_derivative(hidden_layer_output)

        # used to adjust the weights in a way that reduces the error over time.
        W_output += np.dot(hidden_layer_output.T, output_delta) * learning_rate
        B_output += np.sum(output_delta, axis=0) * learning_rate
        W_input += np.dot(X.T, hidden_delta) * learning_rate
        B_input += np.sum(hidden_delta, axis=0) * learning_rate

        # Log loss every 100 epochs
        if (epoch + 1) % 100 == 0:
            loss = np.mean(np.square(y - output))
            print(f'Epoch {epoch+1}, Loss: {loss}')
    
    return W_input, B_input, W_output, B_output

# Predict relevance scores for documents using the trained neural network
def predict_relevance(X, W_input, B_input, W_output, B_output):
    hidden_layer_input = np.dot(X, W_input) + B_input
    hidden_layer_output = sigmoid(hidden_layer_input)
    output_layer_input = np.dot(hidden_layer_output, W_output) + B_output
    output = sigmoid(output_layer_input)
    return output

# Main workflow
query = "Find me articles about the benefits of travelling for health."
folder_path = r'D:\IR\Information-Retrieval-Fall-2024\Assignment 6'

# Preprocess query and expand it
words = preprocess_text(query)
keywords = identify_keywords(words)
expanded_query = expand_query(keywords)

# Retrieve relevant documents based on expanded query
relevant_docs = retrieve_documents(expanded_query, folder_path)

# Display retrieved documents and snippets
for doc in relevant_docs:
    print(f"Document: {doc[0]}, Snippet: {doc[1]}")

# Train neural network and predict relevance scores if documents are found
if relevant_docs:
    X = calculate_relevance_score(relevant_docs)  # Generate feature matrix
    y_train = np.random.randint(0, 2, size=(len(relevant_docs), 1))  # Placeholder labels
    W_input, B_input, W_output, B_output = train_neural_network(X, y_train, epochs=1000, learning_rate=0.01)
    predicted_relevance = predict_relevance(X, W_input, B_input, W_output, B_output)

    # Display predicted relevance scores
    for i, doc in enumerate(relevant_docs):
        print(f"Document: {doc[0]}, Predicted Relevance Score: {predicted_relevance[i][0]:.4f}")
else:
    print("No relevant documents found.")
