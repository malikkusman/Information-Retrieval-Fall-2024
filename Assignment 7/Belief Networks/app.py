from flask import Flask, render_template, request  
from belief_network import BeliefNetwork  

# Initialize Flask application
app = Flask(__name__) 

def load_documents(file_path='documents.txt'):
    """
    Load documents from a text file.
    """
    documents = [] 
    try:
    
        with open(file_path, 'r') as file:
            # Iterate through each line in the file
            for i, line in enumerate(file.readlines(), start=1):
                # Add each line to the documents list, associating it with a unique ID
                documents.append({"id": i, "text": line.strip()})  
        # If no documents were added, raise an error
        if not documents:
            raise ValueError("No documents found in the file.")
    except Exception as e:
        print(f"Error loading documents: {e}")
        return []  
    return documents 

# Initialize the belief network
belief_network = BeliefNetwork()

@app.route('/') 
def index():
    """
    Serve the index page with sample queries and documents.
    """
    documents = load_documents()  
    if not documents:
        return "Error: No documents available. Please check the documents file.", 500  # Error handling if no documents are found

    queries = [
        {"id": 1, "text": "What is machine learning?"}, 
        {"id": 2, "text": "AI applications in healthcare."} 
    ]
    
    return render_template('index.html', queries=queries, documents=documents)

@app.route('/calculate', methods=['POST'])
def calculate():
    """
    Calculate relevance scores for each document based on the user query.
    """
    user_query = request.form['user_query']
    documents = load_documents()  # Load documents again for relevance calculation
    if not documents:
        return "Error: No documents available. Please check the documents file.", 500 

    relevance_scores = {}  # Initialize an empty dictionary to store relevance scores for each document
    for doc in documents:
        # Check if the user query is present in the document text
        # If the query is found, consider the document 'relevant'; otherwise, 'non-relevant'
        doc_feature = "relevant" if user_query.lower() in doc['text'].lower() else "non-relevant"
        # Calculate the relevance score for the document and store it in the dictionary
        relevance_scores[doc['id']] = belief_network.calculate_relevance(user_query, doc_feature)

    # Sort the documents based on relevance scores in descending order
    sorted_documents = sorted(documents, key=lambda doc: relevance_scores[doc['id']], reverse=True)
    return render_template('results.html', query=user_query, documents=sorted_documents, relevance_scores=relevance_scores)

if __name__ == '__main__': 
    app.run(debug=True) 

