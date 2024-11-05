index = {}         
title_index = {}   
documents = {} 

def list_files():
    """
    Manually retrieves list of text file names in the directory.
    This assumes the filenames are provided as a static list for demonstration.
    """
  
    return ["document1.txt", "document2.txt", "document3.txt"]

def read_file(directory_path, filename):
    """
    Reads content from a file in the directory. File paths are manually constructed.
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
    Splits text into individual words (tokens) by manually parsing characters.
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
        words.append(word)  # Add the last word if any
    return words

def build_index(directory_path):
    """
    Reads all files in the directory, processes each document to index
    words for content-based search and titles for title-based search.
    """
    files = list_files()
    for filename in files:
        title = filename.lower()  
        content = read_file(directory_path, filename)
        documents[title] = content
        title_index[title] = filename  

        words = tokenize(content.lower())  
        for word in words:
            if word not in index:
                index[word] = []
            if title not in index[word]:
                index[word].append(title)

def search_by_title(title):
    """
    Searches for a document by title.
    :param title: Title of the document to search for.
    :return: Content of the document if found, or None.
    """
    title = title.lower() 
    return documents.get(title, None)

def search_by_content(query):
    """
    Searches for documents containing words in the query.
    :param query: Search query as a string of words.
    :return: List of document titles containing the query words.
    """
    query_words = tokenize(query.lower())
    matching_docs = []

    for word in query_words:
        if word in index:
            for doc_id in index[word]:
                if doc_id not in matching_docs:
                    matching_docs.append(doc_id)

    return matching_docs

def display_results(docs):
    """
    Prints the document titles that match the search query.
    :param docs: List of document titles (IDs).
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
