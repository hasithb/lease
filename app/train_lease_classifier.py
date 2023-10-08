import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

# Load the data from Excel
df = pd.read_excel('lease_terms_data.xlsx', engine='openpyxl')

# Combine the 'Key Terms' and 'Problem Clauses' data
documents = df['Key Terms'].dropna().tolist() + df['Problem Clauses'].dropna().tolist()

# Labels for the data: 1 for 'Key Terms' and 0 for 'Problem Clauses'
labels = [1]*len(df['Key Terms'].dropna()) + [0]*len(df['Problem Clauses'].dropna())

# Vectorize the text data
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(documents)

# Create a Support Vector Machine (SVM) classifier
classifier = SVC(kernel='linear')

# Train the classifier
classifier.fit(X, labels)

# Save the classifier to a file
joblib.dump(classifier, 'lease_clause_classifier.pkl')

# Save the vectorizer for transforming new documents
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')

print("Classifier and vectorizer saved.")
