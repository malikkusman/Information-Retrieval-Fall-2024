class FuzzyModel:
    def __init__(self, product_file_path):
        """Initialize with product data file."""
        self.products = self.load_product_data(product_file_path)

    def calculate_string_distance(self, str1, str2):
        """
        Calculate the Levenshtein distance between two strings.
        Returns a similarity ratio (0-1).
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

        return 1 - matrix[len_str1][len_str2] / max(len_str1, len_str2)

    def load_product_data(self, file_path):
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

    def calculate_membership_scores(self, query, product):
        """
        Calculate membership scores for a product.
        Compare the query to the product’s name, category, and description.
        """
        name_score = self.calculate_string_distance(query, product["name"])
        category_score = self.calculate_string_distance(query, product["category"])
        description_score = self.calculate_string_distance(query, product["description"])

        return max(name_score, category_score, description_score)

    def process_query(self, query, threshold=0.5):
        """Process the query and return ranked results based on fuzziness threshold."""
        results = []
        for product in self.products:
            relevance = self.calculate_membership_scores(query, product)
            if relevance >= threshold:
                results.append({"product": product, "relevance": relevance})
        # Sort the results by relevance score
        return sorted(results, key=lambda x: x["relevance"], reverse=True)
