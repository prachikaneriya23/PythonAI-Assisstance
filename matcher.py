import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

_STOPWORDS = {
    "the", "a", "an", "is", "are", "how", "do", "does", "to", "in", "of",
    "for", "and", "or", "what", "i", "me", "my", "can", "you", "please",
    "explain", "give", "with", "on", "it", "this", "that", "use", "using",
    "code", "example", "about", "write", "python",
}

class KnowledgeMatcher:
    """A Supervised ML Classifier using TF-IDF features and Logistic Regression."""

    def __init__(self, df: pd.DataFrame):
        self.df = df.reset_index(drop=True)
        
        # Prepare training documents and labels (Categories)
        self.docs = (
            (self.df["keywords"].fillna("") + " ")
            + (self.df["title"].fillna("") + " ") * 2
        ).tolist()
        
        self.labels = self.df["category"].tolist()

        # 1. TF-IDF Feature Extractor Pipeline
        self.vectorizer = TfidfVectorizer(stop_words=list(_STOPWORDS), lowercase=True)
        X = self.vectorizer.fit_transform(self.docs)

        # 2. Train a Supervised Machine Learning Model (Logistic Regression)
        self.classifier = LogisticRegression(max_iter=200)
        self.classifier.fit(X, self.labels)

    def search(self, query: str, top_k: int = 3, min_score: float = 0.05):
        """Classifies query intent using the ML model and returns matching rows."""
        if not query.strip():
            return []
        
        # Transform query using the fitted TF-IDF vectorizer
        q_vec = self.vectorizer.transform([query])
        
        # Get prediction probabilities from the ML model
        probs = self.classifier.predict_proba(q_vec)[0]
        classes = self.classifier.classes_
        
        # Find best matching category based on ML confidence
        best_idx = np.argmax(probs)
        best_category = classes[best_idx]
        confidence = probs[best_idx]

        # Fallback or match rows within that predicted category or overall similarity
        # To keep it compatible with your existing UI, we score rows based on class match + keyword overlap
        results = []
        for i, row in self.df.iterrows():
            doc_vec = self.vectorizer.transform([self.docs[i]])
            score = float((q_vec @ doc_vec.T).toarray()[0, 0])
            
            # Boost score if category matches the ML model's prediction
            if row["category"] == best_category:
                score += 0.2
                
            if score >= min_score:
                results.append((score, row))
                
        # Sort by score descending
        results.sort(key=lambda x: x[0], reverse=True)
        return results[:top_k]