import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer

module_dir = os.path.dirname(__file__)

model_path = os.path.join(module_dir, 'model.pkl')
vectorizer_path = os.path.join(module_dir, 'tfidf_vectorizer.pkl')

with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)

with open(vectorizer_path, 'rb') as vectorizer_file:
    tfidf_vectorizer = pickle.load(vectorizer_file)

def predict_abusiveness(text):
    tfidf_text = tfidf_vectorizer.transform([text])
    abusiveness_score = model.predict_proba(tfidf_text)[0]
    return abusiveness_score[0], abusiveness_score[1]

def predict_abusiveness_file(input_file, output_file):
    with open(input_file, 'r') as file:
        kalimat_list = file.read().splitlines()

    with open(output_file, 'w') as output:
        for kalimat in kalimat_list:
            tfidf_text = tfidf_vectorizer.transform([kalimat])
            abusiveness_score = model.predict_proba(tfidf_text)[0]
            output.write(f"{kalimat}\n")
            output.write(f"Positive: {abusiveness_score[0]:.2f}, Negative: {abusiveness_score[1]:.2f}\n\n")
    print(f"The abuse prediction results have been saved in a file: {output}")