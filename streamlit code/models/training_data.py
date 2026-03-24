import pandas as pd
import os
import pickle
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
# from nlp.text_cleaner import clean_text  # Avoid import cycle

# Load training data
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'trainning_data.csv')
df = pd.read_csv(data_path)
print(f"Loaded {len(df)} training samples")
print(df['job_role'].value_counts())

# Preprocess (local clean function to avoid import)
def simple_clean(text):
    text = str(text).lower()
    text = re.sub(r'\\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\\s+', ' ', text).strip()
    return text

df['clean_text'] = df['text'].apply(simple_clean)
X = df['clean_text']
y = df['job_role']

import string  # Move up for simple_clean

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1,2))),
    ('classifier', MultinomialNB())
])

# Train
pipeline.fit(X_train, y_train)

# Evaluate
y_pred = pipeline.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print(classification_report(y_test, y_pred))

# Save model
model_path = os.path.join(os.path.dirname(__file__), 'nlp_model.pkl')
with open(model_path, 'wb') as f:
    pickle.dump(pipeline, f)
print(f"Model saved to {model_path}")

# Test prediction
test_resume = "python machine learning data scientist pandas numpy"
pred = pipeline.predict([test_resume])[0]
print(f"Test prediction: {pred}")

