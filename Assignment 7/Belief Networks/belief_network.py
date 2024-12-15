class BeliefNetwork:
    def __init__(self):
        # Set prior probabilities for the query and document relevance
        self.p_query = 0.5  
        self.p_relevance = 0.5 
        
        # Set conditional probabilities for the query and relevance
        self.p_query_given_relevance = 0.8  
        self.p_relevance_given_query = 0.9
        
        # Set probabilities for document features given relevance or non-relevance
        self.p_doc_feature_given_relevance = 0.7 
        self.p_doc_feature_given_non_relevance = 0.3

    def bayesian_update(self):
        """
        Perform Bayesian update to calculate the posterior probability of relevance given the query.
        """
        p_relevance_given_query = (self.p_query_given_relevance * self.p_relevance) / self.p_query
        return p_relevance_given_query  # Return the computed posterior probability

    def joint_probability(self):
        # Calculate the joint probability of the query and relevance using the formula
        # P(Query, Relevance) = P(Query | Relevance) * P(Relevance)
        return self.p_query_given_relevance * self.p_relevance  # Return the joint probability

    def marginal_probability(self):
        # Return the prior probability of relevance
        return self.p_relevance  

    def relevance_given_feature(self, doc_feature):
        """
        Calculate the conditional probability of relevance given a document feature.
        """
        # If the document feature is "relevant", use the corresponding probability for relevance
        if doc_feature == "relevant":
            return self.p_relevance_given_query * self.p_doc_feature_given_relevance
        else:
            # If the document feature is "non-relevant", use the non-relevant feature probability
            return (1 - self.p_relevance_given_query) * self.p_doc_feature_given_non_relevance

    def calculate_relevance(self, query, doc_feature):
        """
        Calculate the final relevance score of a document based on the query and document feature.
        """
        p_relevance = self.bayesian_update()
        
        # Calculate the conditional probability of relevance given the document feature
        p_feature_given_relevance = self.relevance_given_feature(doc_feature)
        
        # Multiply the posterior probability of relevance with the feature probability to calculate final relevance
        final_relevance = p_relevance * p_feature_given_relevance
        
        return final_relevance  
