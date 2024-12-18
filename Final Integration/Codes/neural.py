import numpy as np
import nltk
from nltk.corpus import wordnet
import os

# Download required NLTK data for tokenization
nltk.download('punkt')


class NeuralNetwork:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def preprocess_text(self, query):
        """Converts the query to lowercase and tokenizes it into words."""
        words = nltk.word_tokenize(query.lower())
        return words

    def identify_keywords(self, words):
        """Filters out non-alphabetic words to retain important keywords."""
        important_keywords = [word for word in words if word.isalpha()]
        return important_keywords

    def get_synonyms(self, word):
        """Uses WordNet to find synonyms for each keyword, enhancing query coverage."""
        synonyms = set()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name())
        return list(synonyms)

    def expand_query(self, keywords):
        """Combines keywords and their synonyms into an expanded list."""
        expanded_query = []
        for word in keywords:
            expanded_query.append(word)
            synonyms = self.get_synonyms(word)
            expanded_query.extend(synonyms)
        return expanded_query

    def retrieve_documents(self, expanded_query):
        """Retrieves relevant documents by matching expanded query terms with the text content in files."""
        relevant_documents = []
        for filename in os.listdir(self.folder_path):
            if filename.endswith('.txt'):
                with open(os.path.join(self.folder_path, filename), 'r', encoding='utf-8') as file:
                    doc_text = file.read().lower()
                    for term in expanded_query:
                        if term in doc_text:
                            relevant_documents.append((filename, doc_text[:200]))
                            break
        return relevant_documents

    @staticmethod
    def calculate_relevance_score(relevant_docs):
        """Generates random relevance scores for retrieved documents."""
        num_docs = len(relevant_docs)
        X = np.random.rand(num_docs, 10)
        return X

    @staticmethod
    def sigmoid(x):
        """Activation function for neural network layers."""
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def sigmoid_derivative(x):
        """Derivative of sigmoid function for backpropagation."""
        return x * (1 - x)

    def train_neural_network(self, X, y, epochs, learning_rate):
        """Trains a simple neural network."""
        input_size = X.shape[1]
        hidden_size = 8
        output_size = 1

        W_input = np.random.randn(input_size, hidden_size) * 0.1
        B_input = np.zeros((1, hidden_size))
        W_output = np.random.randn(hidden_size, output_size) * 0.1
        B_output = np.zeros((1, output_size))

        for epoch in range(epochs):
            hidden_layer_input = np.dot(X, W_input) + B_input
            hidden_layer_output = self.sigmoid(hidden_layer_input)
            output_layer_input = np.dot(hidden_layer_output, W_output) + B_output
            output = self.sigmoid(output_layer_input)

            output_error = y - output
            output_delta = output_error * self.sigmoid_derivative(output)
            hidden_error = np.dot(output_delta, W_output.T)
            hidden_delta = hidden_error * self.sigmoid_derivative(hidden_layer_output)

            W_output += np.dot(hidden_layer_output.T, output_delta) * learning_rate
            B_output += np.sum(output_delta, axis=0) * learning_rate
            W_input += np.dot(X.T, hidden_delta) * learning_rate
            B_input += np.sum(hidden_delta, axis=0) * learning_rate

            if (epoch + 1) % 100 == 0:
                loss = np.mean(np.square(y - output))
                print(f'Epoch {epoch + 1}, Loss: {loss}')

        return W_input, B_input, W_output, B_output

    def predict_relevance(self, X, W_input, B_input, W_output, B_output):
        """Predicts relevance scores for documents."""
        hidden_layer_input = np.dot(X, W_input) + B_input
        hidden_layer_output = self.sigmoid(hidden_layer_input)
        output_layer_input = np.dot(hidden_layer_output, W_output) + B_output
        output = self.sigmoid(output_layer_input)
        return output

