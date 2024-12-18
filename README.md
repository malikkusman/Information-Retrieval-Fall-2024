# Information Retrieval (IR) Models Overview

This project focuses on building and understanding various Information Retrieval (IR) models to retrieve relevant documents based on keyword search. It covers basic and advanced techniques to enhance document ranking and retrieval accuracy.

## Objectives
- Develop a basic document search engine.
- Implement ranking mechanisms for relevance-based document retrieval.

## Key Features
1. **Keyword Matching**:
   - Matches query terms with document terms.
   - Limitation: Only considers exact matches, ignoring synonyms and context.

2. **TF-IDF Scoring**:
   - **Term Frequency (TF)**: Measures the frequency of terms in a document.
   - **Inverse Document Frequency (IDF)**: Evaluates the uniqueness of terms across all documents.
   - Combined TF-IDF: Ranks documents by their importance based on query terms.

3. **Cosine Similarity**:
   - Measures the cosine of the angle between two vectors (query vs. document) to determine their similarity.

## Information Retrieval Models
1. **Structured Models**:
   - Organizes documents using structured data for easier navigation.

2. **Non-Overlapped List Model**:
   - Matches terms from queries with non-overlapping document lists.

3. **Proximal Nodes Model**:
   - Represents documents as nodes in a graph, focusing on term proximity.

4. **Set-Theoretic Models**:
   - **Boolean Model**: Matches documents based on Boolean logic.
   - **Extended Boolean Model**: Incorporates fuzzy logic for partial matching.
   - **Fuzzy IR Model**: Handles imprecise queries using fuzzy logic.

5. **Hypertext Model**:
   - Links documents via hypertext for web-like navigation.

6. **Probabilistic Models**:
   - **Belief Network Model**: Uses probabilistic reasoning to determine relevance.

7. **Neural Network Models**:
   - Leverages deep learning (e.g., CNNs, RNNs, transformers) for semantic understanding and contextual relevance.

## Evolution of IR Models
The field of IR has evolved from simple keyword-based methods to advanced neural network techniques, enabling improved accuracy and relevance in document retrieval.

## Contributors
- **Usama Mehboob (2021-CS-10)**
- **Hamza Rasheed (2021-CS-26)**
- **Bilal Baig (2021-CS-36)**
- **Usman Asghar (2021-CS-46)**

### Supervisor
- Prof. Dr. Khaldoon Khurshid

---
