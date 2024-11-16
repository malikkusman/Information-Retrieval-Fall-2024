class DocumentList:
    """
    storing and retrive of docuemnents by title and content
    """
    def __init__(self):
        self.documents = [] 
        

    def add_document(self, title, content):
        self.documents.append((title, content))

    def find_document(self, title):
        for doc_title, content in self.documents:
            if doc_title == title:
                return content
        return None


class Index:
    
    """
    creating an index of words (terms) and it links with document titles.
    """
    def __init__(self):
        self.index = []

    def add_word(self, word, document_title):
        """
        adds a word to the index, associating it with a document title
        """
        for i in range(len(self.index)):
            if self.index[i][0] == word:
                if document_title not in self.index[i][1]:
                    self.index[i][1].append(document_title)
                return
        # If word is not found, add new word with document title
        self.index.append((word, [document_title]))

    def get_documents(self, word):
        for term, doc_list in self.index:
            if term == word:
                return doc_list
        return []


documents = DocumentList()
index = Index()


def list_files():
    """
    Manually retrieves list of text file names in the directory.
    """
    return ["document1.txt", "document2.txt", "document3.txt" , "document4.txt" , "document5.txt"]


def read_file(directory_path, filename):
    """
    Reads content from a file in the directory.
    """
    path = directory_path + '/' + filename
    content = ""
    try:
        with open(path, 'r') as file:
            for line in file:
                content += line.strip() + " "
    except FileNotFoundError:
        print(f"File {filename} not found in directory.")
    return content


def tokenize(text):
    """
    Splits text into individual words (tokens).
    """
    words = []
    word = ""
    for char in text:
        if 'a' <= char <= 'z' or '0' <= char <= '9':
            word += char
        else:
            if word:
                words.append(word)
                word = ""
    if word:
        words.append(word)
    return words


def build_index(directory_path):
    """
    processes all files in the directory, reading their content and creating both a document lis, an index. 
    """
    files = list_files()
    for filename in files:
        title = filename.lower()
        content = read_file(directory_path, filename)
        documents.add_document(title, content)
        words = tokenize(content.lower())
        for word in words:
            index.add_word(word, title)


def search_by_title(title):
    """
    Searches for a document by title.
    """
    title = title.lower()
    return documents.find_document(title)


def search_by_content(query):
    """
    Searches for documents containing words in the query.
    """
    query_words = tokenize(query.lower())
    matching_docs = []
    for word in query_words:
        doc_list = index.get_documents(word)
        for doc in doc_list:
            if doc not in matching_docs:
                matching_docs.append(doc)
    return matching_docs


def display_results(docs):
    """
    Prints the document titles that match the search query.
    """
    if not docs:
        print("No documents found matching your query.")
    else:
        print("Documents found:")
        for doc_id in docs:
            print(f"- {doc_id}")


if __name__ == "__main__":
    directory_path = "D:\\IR\\Information-Retrieval-Fall-2024\\Assignment 1"
    build_index(directory_path)

    while True:
        print("\nSimple Document Search Engine")
        print("1. Search by Title")
        print("2. Search by Content")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            title = input("Enter the document title: ")
            content = search_by_title(title)
            if content:
                print("\nDocument Content:")
                print(content)
            else:
                print("Document not found.")
        elif choice == '2':
            query = input("Enter search terms: ")
            matching_docs = search_by_content(query)
            display_results(matching_docs)
        elif choice == '3':
            print("Exiting the search engine.")
            break
        else:
            print("Invalid choice. Please try again.")
