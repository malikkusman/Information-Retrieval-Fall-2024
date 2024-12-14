from flask import Flask, render_template, request

#

app = Flask(__name__)

def calculate_string_distance(str1, str2):
    """
    This function calculates the Levenshtein distance between two strings
    """
    len_str1 = len(str1)
    len_str2 = len(str2)
    matrix = [[0] * (len_str2 + 1) for _ in range(len_str1 + 1)]

    for i in range(len_str1 + 1):
        matrix[i][0] = i
    for j in range(len_str2 + 1):
        matrix[0][j] = j

    for i in range(1, len_str1 + 1):
        for j in range(1, len_str2 + 1):
            cost = 0 if str1[i - 1] == str2[j - 1] else 1
            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + cost)

    return 1 - matrix[len_str1][len_str2] / max(len_str1, len_str2)  # Returns similarity ratio (0-1)

def load_product_data(file_path):
    """Load product data from a txt file."""
    products = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            product_info = line.strip().split('|')
            product = {
                'id': int(product_info[0].strip()),
                'name': product_info[1].strip(),
                'category': product_info[2].strip(),
                'description': product_info[3].strip()
            }
            products.append(product)
    return products

def calculate_membership_scores(query, product):
    """
    Calculate membership scores for a product.
    it compares the query to the product’s name, category, and description
    """
    name_score = calculate_string_distance(query, product["name"])
    category_score = calculate_string_distance(query, product["category"])
    description_score = calculate_string_distance(query, product["description"])

    return max(name_score, category_score, description_score)

def process_query(query, products, threshold=0.5):
    """Process the query and return ranked results based on fuzziness threshold."""
    results = []
    for product in products:
        relevance = calculate_membership_scores(query, product)
        if relevance >= threshold:
            results.append({"product": product, "relevance": relevance})
    # Sort the results by relevance score
    return sorted(results, key=lambda x: x["relevance"], reverse=True)

@app.route("/", methods=["GET", "POST"])
def index():
    products = load_product_data('products.txt')
    results = []
    threshold = 0.5  # default threshold

    if request.method == "POST":
        query = request.form.get('query')
        threshold = float(request.form.get('threshold', 0.5))  # fuzziness threshold
        results = process_query(query, products, threshold)

    return render_template("index.html", results=results, threshold=threshold)

if __name__ == "__main__":
    app.run(debug=True)
