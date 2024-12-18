from flask import Flask, render_template, request, jsonify, redirect, url_for
from Codes.SearchEngine import SearchEngine
from Codes.RankingSystem import RankingSystem
from Codes.BIM import BinaryIndependenceModel
from Codes.NOL import NonOverlappedListModel
from Codes.PN import ProximalNodesModel
from Codes.fuzzy import FuzzyModel
from Codes.neural import NeuralNetwork
import json

app = Flask(__name__)

# Paths to document folders
DOCUMENT_FOLDER = "D:\\IR\\Information-Retrieval-Fall-2024\\Final Integration\\Codes\\Docs"
DOCUMENT_FOLDERS = "D:\\IR\\Information-Retrieval-Fall-2024\\Final Integration\\Codes\\Structured_Docs"
Product_Folder = "D:\\IR\\Information-Retrieval-Fall-2024\\Final Integration\\Codes\\Product\\products.txt"
Neural_Folder = "D:\\IR\\Information-Retrieval-Fall-2024\\Final Integration\\Codes\\NeuralDocs"

# Load document data from JSON
with open("Codes/Data/data.json", "r") as file:
    documents = json.load(file)

# Load JSON data
def load_students():
    with open('Codes/Data/structuredata.json') as f:
        return json.load(f)

# Initialize system components
search_engine = SearchEngine(DOCUMENT_FOLDER)
ranking_system = RankingSystem(DOCUMENT_FOLDER)
binary_independence_model = BinaryIndependenceModel(DOCUMENT_FOLDER)
non_overlapped = NonOverlappedListModel(DOCUMENT_FOLDER)
model = ProximalNodesModel()
fuzzy = FuzzyModel(Product_Folder)
neural = NeuralNetwork(Neural_Folder)

# Prepare models and data
model.build_network(DOCUMENT_FOLDERS)
non_overlapped.build_term_document_map()
search_engine.load_documents()
binary_independence_model.load_documents()

@app.route("/neural", methods=["GET", "POST"])
def neural_route():
    if request.method == "POST":
        query = request.form.get("query")
        return redirect(url_for("neural_app", query=query))  # Correct endpoint name
    return render_template("neural.html")


@app.route("/neural_app")
def neural_app():  # Renamed to match the endpoint
    query = request.args.get("query", "")
    ir_system = NeuralNetwork(Neural_Folder)

    # Process and expand query
    words = ir_system.preprocess_text(query)
    keywords = ir_system.identify_keywords(words)
    expanded_query = ir_system.expand_query(keywords)

    # Retrieve documents
    relevant_docs = ir_system.retrieve_documents(expanded_query)
    return render_template("neural_results.html", query=query, results=relevant_docs)




@app.route("/fuzzy", methods=["GET", "POST"])
def fuzzy_route():
    products = fuzzy.products  # Access the products directly from the FuzzyModel instance
    results = []
    threshold = 0.5  # default threshold

    if request.method == "POST":
        query = request.form.get('query')
        threshold = float(request.form.get('threshold', 0.5))  # fuzziness threshold
        results = fuzzy.process_query(query, threshold)

    return render_template("fuzzy.html", results=results, threshold=threshold)



@app.route('/structure')
def structure_guided():
    students_data = load_students()
    return render_template('structure.html', students=students_data)

@app.route('/student/<int:student_id>')
def get_student_data(student_id):
    students_data = load_students()
    student = next((s for s in students_data if s['Id'] == student_id), None)
    return jsonify(student)

@app.route("/hypertext")
def hypertext_page():
    return render_template("hyper_text.html")

@app.route("/get-doc/<doc_id>")
def get_document(doc_id):
    """
    Retrieve a document by its ID.
    """
    doc = next((doc for doc in documents if doc["id"] == doc_id), None)
    if doc:
        return jsonify(doc)
    return jsonify({"error": "Document not found"}), 404

@app.route("/get-graph")
def get_graph():
    """
    Build and return a graph representation of the documents.
    """
    nodes = [{"id": doc["id"]} for doc in documents]
    links = []

    for doc in documents:
        for word in doc["content"].split():
            if word.startswith("[") and word.endswith(")"):
                target_id = word[word.find("(") + 1 : word.find(")")]
                if target_id != doc["id"]:  # Avoid self-loops
                    links.append({"source": doc["id"], "target": target_id})

    return jsonify({"nodes": nodes, "links": links})

@app.route("/proximalnodes", methods=["GET", "POST"])
def proximal_nodes():
    """
    Handle queries for the Proximal Nodes model.
    """
    if request.method == "POST":
        query = request.form.get("query")
        proximal_nodes = query.lower().split(",")
        results = model.retrieve_connected_documents(proximal_nodes)
        return render_template("PNresults.html", nodes=proximal_nodes, results=results)
    return render_template("PN.html")

@app.route("/nonoverlapped")
def non_overlapping_list_page():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search_non_overlapping():
    """
    Search using the Non-Overlapping List model.
    """
    terms_input = request.form.get("terms")
    terms_of_interest = [term.strip() for term in terms_input.split(",")]
    results = non_overlapped.retrieve_non_overlapping_documents(terms_of_interest)
    return jsonify({"documents": list(results)})

@app.route("/rank", methods=["GET", "POST"])
def search():
    """
    Homepage with search functionality.
    """
    if request.method == "POST":
        query = request.form["query"]
        search_type = request.form.get("search_type", "content")
        ranking_method = request.form.get("ranking_method", "keyword")

        if not query:
            return render_template("search.html", error="Please enter a query.")

        # Perform search and ranking based on the selected method
        if ranking_method == "keyword":
            results = ranking_system.rank_by_keyword_matching(query)
        elif ranking_method == "tfidf":
            results = ranking_system.rank_by_tfidf(query)
        elif ranking_method == "cosine":
            results = ranking_system.rank_by_cosine_similarity(query)
        elif ranking_method == "bim":
            results = binary_independence_model.retrieve_top_k_documents(query, k=5)
        else:
            results = []

        # Format results for better UI
        formatted_results = []
        for filename, score in results:
            doc = search_engine.documents.get(filename)
            if doc:
                title = doc.get("title", filename)
                snippet = " ".join(doc["content"].split()[:15]) + "..."
                formatted_results.append((title, snippet, f"{score:.5f}"))


        return render_template(
            "results.html", query=query, results=formatted_results, method=ranking_method
        )

    return render_template("search.html")


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        query = request.form.get('query')
        search_type = request.form.get('search_type')
        results = search_engine.search(query, search_type=search_type)
        return render_template('searchengine.html', query=query, search_type=search_type, results=results)

    # Render the page initially with an empty form or any default content
    return render_template('searchengine.html')

if __name__ == "__main__":
    app.run(debug=True)
