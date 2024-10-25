# Step 1: Define Document Folder Path
DOCUMENT_FOLDER = "./documents/"  # Path to the folder containing the documents

# Step 2: Utility Function for Cleaning and Preprocessing Text (No Built-in Libraries)
def clean_text(text):
    """
    This function manually cleans the input text by converting it to lowercase,
    removing punctuation, and splitting into individual words.
    """
    text = text.lower()  # Convert text to lowercase
    cleaned_text = ""
    # Manually remove punctuation
    for char in text:
        if 'a' <= char <= 'z' or char == ' ':
            cleaned_text += char
    words = cleaned_text.split()  # Split text into words
    return words

# Step 3: Function to Read Files (No Built-in Libraries)
def read_file(file_path):
    """
    This function manually reads the content of a file line by line.
    """
    content = ""
    with open(file_path, 'r') as file:
        for line in file:
            content += line
    return content

# Step 4: Function to Get File Names in a Folder (Without using os.listdir)
def get_file_names():
    """
    Manually gets the list of document file names in the documents folder.
    (This assumes the user will manually provide the file names.)
    """
    return ['doc1.txt', 'doc2.txt', 'doc3.txt']  # Example file names, manually entered

# Step 5: Function to Build Title Index and Inverted Index with Positions
def build_indexes():
    """
    This function creates two indexes:
    1. title_index: a dictionary mapping document titles to file names.
    2. inverted_index: a dictionary mapping words to the list of file names (documents) where they appear.
       It also stores the positions of the words in the document for phrase search.
    """
    title_index = {}  # Document title to file mapping
    inverted_index = {}  # Word to document mapping with positions
    documents = {}  # To store original words for each document
    
    # Loop through all files in the document folder
    file_names = get_file_names()
    for file_name in file_names:
        file_path = DOCUMENT_FOLDER + file_name  # Construct the full file path
        content = read_file(file_path)
        
        # Extract title from the first line of the file
        lines = content.split('\n')  # Split content by lines
        title = lines[0].strip()
        title_index[title.lower()] = file_name  # Store title in lowercase for case-insensitive search
        
        # Process the rest of the document for indexing
        words = clean_text(content)
        documents[file_name] = words  # Store original words for each document
        
        # Build the inverted index manually with word positions
        for pos, word in enumerate(words):
            if word not in inverted_index:
                inverted_index[word] = {file_name: [pos]}  # Add new entry with positions
            else:
                if file_name not in inverted_index[word]:
                    inverted_index[word][file_name] = [pos]
                else:
                    inverted_index[word][file_name].append(pos)

    # Compress the index by storing position differences (gaps)
    for word in inverted_index:
        for file_name in inverted_index[word]:
            positions = inverted_index[word][file_name]
            # Store the differences instead of absolute positions
            compressed_positions = []
            previous_pos = -1
            for pos in positions:
                compressed_positions.append(pos - previous_pos)
                previous_pos = pos
            inverted_index[word][file_name] = compressed_positions

    return title_index, inverted_index, documents

# Step 6: Search Function by Title
def search_by_title(query, title_index):
    """
    This function searches for a document by its title.
    :param query: The title to search for
    :param title_index: The dictionary that maps titles to file names
    :return: The document file name or a message if not found
    """
    query = query.strip().lower()  # Case-insensitive search
    if query in title_index:
        return f"Document found: {title_index[query]}"
    else:
        return "No document found with that title."

# Step 7: Search Function by Phrase (Exact Phrase Match)
def search_by_phrase(query, inverted_index, documents):
    """
    This function searches for documents that contain an exact phrase.
    :param query: The phrase to search for
    :param inverted_index: The dictionary that maps words to documents and positions
    :param documents: The original words of each document for phrase matching
    :return: A list of documents that contain the phrase or a message if not found
    """
    query_words = clean_text(query)
    
    if len(query_words) == 0:
        return "No phrase provided for search."
    
    # Check if the first word of the phrase is in the index
    first_word = query_words[0]
    if first_word not in inverted_index:
        return f"No document contains the phrase '{query}'."
    
    potential_docs = inverted_index[first_word]
    matching_docs = []
    
    # For each document where the first word appears, check if the rest of the phrase matches
    for doc, compressed_positions in potential_docs.items():
        # Decode the compressed positions back to absolute positions
        positions = []
        current_pos = 0
        for gap in compressed_positions:
            current_pos += gap
            positions.append(current_pos)

        # Get the original words for the current document
        words = documents[doc]
        
        # Check if the subsequent words in the phrase match in the document
        for pos in positions:
            match = True
            for i in range(1, len(query_words)):
                if pos + i >= len(words) or words[pos + i] != query_words[i]:
                    match = False
                    break
            if match:
                matching_docs.append(doc)
                break  # We found a match, no need to check further positions
    
    if matching_docs:
        return f"Phrase '{query}' found in documents: {', '.join(matching_docs)}"
    else:
        return f"No document contains the exact phrase '{query}'."

# Step 8: Search Function by Content (Word Search)
def search_by_content(query, inverted_index):
    """
    This function searches for documents that contain a specific word in their content.
    :param query: The word to search for
    :param inverted_index: The dictionary that maps words to documents
    :return: A list of documents that contain the word or a message if not found
    """
    query = query.strip().lower()
    if query in inverted_index:
        return f"Word '{query}' found in documents: {', '.join(inverted_index[query].keys())}"
    else:
        return f"No document contains the word '{query}'."

# Step 9: The Main Program for User Interaction
def main():
    """
    Main function to interact with the user and allow searches by title, word, or phrase.
    """
    # Build the indexes from the documents in the folder
    title_index, inverted_index, documents = build_indexes()

    while True:
        print("\n=== Simple Document Search Engine ===")
        print("1. Search by Document Title")
        print("2. Search by Document Content (Word Search)")
        print("3. Search by Exact Phrase")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ").strip()

        if choice == '1':
            # Search by title
            query = input("Enter the document title to search: ").strip()
            result = search_by_title(query, title_index)
            print(result)

        elif choice == '2':
            # Search by word in content
            query = input("Enter a word to search in document contents: ").strip()
            result = search_by_content(query, inverted_index)
            print(result)

        elif choice == '3':
            # Search by exact phrase
            query = input("Enter the phrase to search for: ").strip()
            result = search_by_phrase(query, inverted_index, documents)
            print(result)

        elif choice == '4':
            # Exit the search engine
            print("Exiting the search engine. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

# Run the main program
if __name__ == "__main__":
    main()
