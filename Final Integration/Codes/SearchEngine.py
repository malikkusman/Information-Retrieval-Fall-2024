import os
import string
from nltk.stem import WordNetLemmatizer


class Node:
    """Node class to store key-value pairs in a linked list for handling collisions."""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class CustomDictionary:
    """Custom dictionary data structure with basic hash table implementation."""

    def __init__(self, size=500):
        self.size = size
        self.table = [None] * self.size

    def _hash(self, key):
        """Hashes the key to an index based on the size of the table."""
        return hash(key) % self.size

    def insert(self, key, value):
        """Inserts a key-value pair into the dictionary."""
        index = self._hash(key)
        if not self.table[index]:
            self.table[index] = Node(key, value)
        else:
            current = self.table[index]
            while current:
                if current.key == key:
                    current.value = value  # Update existing key
                    return
                if not current.next:
                    break
                current = current.next
            current.next = Node(key, value)  # Insert new node at the end

    def get(self, key):
        """Retrieves the value associated with the given key."""
        index = self._hash(key)
        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        raise KeyError(f"Key '{key}' not found.")

    def items(self):
        """Yields key-value pairs stored in the dictionary."""
        for node in self.table:
            current = node
            while current:
                yield current.key, current.value
                current = current.next

    def delete(self, key):
        """Deletes a key-value pair from the dictionary."""
        index = self._hash(key)
        current = self.table[index]
        prev = None
        while current:
            if current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self.table[index] = current.next
                return
            prev = current
            current = current.next
        raise KeyError(f"Key '{key}' not found.")

    def __repr__(self):
        """Returns a string representation of the dictionary."""
        items = []
        for i, node in enumerate(self.table):
            while node:
                items.append(f"{node.key}: {node.value}")
                node = node.next
        return "{" + ", ".join(items) + "}"


class SearchEngine:
    """
    A simple document search engine that indexes and searches text files in a specified directory.

    Attributes:
        directory (str): Directory containing the text documents.
        documents (dict): Stores document title and content.
        content_index (dict): Index for content-based word search.
        title_index (dict): Index for title-based word search.
        stop_words (set): Common stop words to exclude from indexing.
    """
    def __init__(self, directory):
        """
        Initializes the search engine with the directory to load documents from.

        Args:
            directory (str): Directory path containing text files to be indexed.
        """
        self.directory = directory
        self.documents = CustomDictionary()  # Stores document title and content
        self.content_index = CustomDictionary()    # Index for content words
        self.title_index = CustomDictionary()      # Index for title words
        self.stop_words = set([
            "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", 
            "in", "into", "is", "it", "no", "not", "of", "on", "or", "such", 
            "that", "the", "their", "then", "there", "these", "they", "this", 
            "to", "was", "will", "with", "from"
        ]) # Stop words to reomve

    def load_documents(self):
        """
        Loads documents from the directory, reading titles and contents, and indexes them by title and content.
        """
        file_path = os.path.join(os.path.dirname(__file__), self.directory)
        for filename in os.listdir(file_path):
            if filename.endswith(".txt"): # Reading .txt files
                with open(os.path.join(file_path, filename), 'r', encoding='utf-8') as file:
                    # Arranging the text in the file
                    doc = file.read().split("\n", 1)
                    title = doc[0].replace("Title: ", "")
                    content = doc[1].replace("Content: ", "")
                    self.documents.insert(filename, {"title": title, "content": content})
                    # Index both title and content
                    self.index(filename, title, self.title_index)
                    self.index(filename, content, self.content_index)

    def filter_nouns(self, words):
        """
        Filters words and returns only those that likely represent nouns.
        
        Args:
            words (list): List of words to filter.
        
        Returns:
            list: List of words that are likely nouns.
        """
        noun_suffixes = {"tion", "ness", "ity", "ment", "er", "ism", "age", "ship", "ence", "ance"}
        articles = {"a", "an", "the"}
        
        nouns = []
        for i, word in enumerate(words):
            # Rule 1: Check if the word follows an article
            if i > 0 and words[i - 1].lower() in articles:
                nouns.append(word)
                continue

            # Rule 2: Check for capitalization (assuming proper nouns at start of sentence excluded)
            if word[0].isupper():
                nouns.append(word)
                continue

            # Rule 3: Check for common noun suffixes
            if any(word.endswith(suffix) for suffix in noun_suffixes):
                nouns.append(word)

        return nouns

    def preprocess_text(self, text):
        """
        Converts text to lowercase, removes punctuation, and excludes stop words.

        Args:
            text (str): The text to be processed.
        
        Returns:
            list: List of processed words.
        """
        lemmatizer = WordNetLemmatizer()
        text = text.translate(str.maketrans('', '', string.punctuation))
        all_words = text.split()
        nouns = [lemmatizer.lemmatize(noun.lower()) for noun in self.filter_nouns(all_words)] # Selecting the nouns
        words = [lemmatizer.lemmatize(word.lower()) for word in all_words if word.lower() not in self.stop_words] # Removing Stop words
        return words + nouns

    def preprocess_query(self, text):
        """
        Converts text to lowercase, removes punctuation, and excludes stop words.

        Args:
            text (str): The text to be processed.
        
        Returns:
            list: List of processed words.
        """
        lemmatizer = WordNetLemmatizer()
        text = text.lower().translate(str.maketrans('', '', string.punctuation))
        words = [lemmatizer.lemmatize(word) for word in text.split() if word not in self.stop_words]
        return words

    def index(self, filename, content, index):
        """
        Indexes words from the content, storing their frequencies.

        Args:
            filename (str): The document filename.
            content (str): The document content.
            index (dict): The index to update (title or content index).
        """
        words = self.preprocess_text(content)
        word_counts = {}
        
        # Count how many times each word occur in one file
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1

        # Creating the index word by word with thier filename and count
        for word, count in word_counts.items():
            try:
                existing = index.get(word)
            except KeyError:
                existing = CustomDictionary()
                index.insert(word, existing)
            existing.insert(filename, count)

    def search(self, query, search_type="content"):
        """
        Searches for the query in the specified index and ranks results by relevance score.

        Args:
            query (str): The search query.
            search_type (str): Either 'content' or 'title', determining the search index.

        Returns:
            list: Sorted list of matching documents with filenames, titles, snippets, and scores.
        """
        words = self.preprocess_query(query)
        matching_documents = CustomDictionary() # Dictionary to store document scores

        # Selecting the index base on search type
        index = self.title_index if search_type == "title" else self.content_index
        for word in words:
            try:
                docs_with_word = index.get(word)
                for filename, freq in docs_with_word.items():  # Use items() to get key-value pairs
                    try:
                        score = matching_documents.get(filename) + freq
                        matching_documents.insert(filename, score)
                    except KeyError:
                        matching_documents.insert(filename, freq)
            except KeyError:
                continue

        # Sort documents by the relevance score (higher score first)
        sorted_results = sorted(
            [(filename, score) for filename, score in matching_documents.items() if filename],
            key=lambda item: item[1], reverse=True
        )
        
        results = []
        for filename, score in sorted_results:
            doc = self.documents.get(filename)
            title = doc["title"]
            snippet = ' '.join(doc["content"].split()[:15]) + "........."  # First 15 words as snippet
            results.append((filename, title, snippet, score))
        return results

