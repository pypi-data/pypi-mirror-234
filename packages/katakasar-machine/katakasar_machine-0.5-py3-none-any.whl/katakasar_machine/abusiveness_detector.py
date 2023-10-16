import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer

# Dapatkan direktori saat modul ini berada
module_dir = os.path.dirname(__file__)

# Path lengkap ke file model.pkl
model_path = os.path.join(module_dir, 'model.pkl')
vectorizer_path = os.path.join(module_dir, 'tfidf_vectorizer.pkl')

# Load model dari file pickle
with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)

# Load TF-IDF Vectorizer dari file pickle
with open(vectorizer_path, 'rb') as vectorizer_file:
    tfidf_vectorizer = pickle.load(vectorizer_file)

# Fungsi untuk menghitung skor abusiveness dari teks
def predict_abusiveness(text):
    # Transformasi teks input ke dalam representasi TF-IDF
    tfidf_text = tfidf_vectorizer.transform([text])

    # Prediksi skor abusiveness
    abusiveness_score = model.predict_proba(tfidf_text)[0]

    # Mengembalikan skor positif dan negatif
    return abusiveness_score[0], abusiveness_score[1]

# Fungsi untuk memprediksi abusiveness dari file teks
def predict_abusiveness_file(input_file, output_file):
    with open(input_file, 'r') as file:
        kalimat_list = file.read().splitlines()

    with open(output_file, 'w') as output:
        for kalimat in kalimat_list:
            tfidf_text = tfidf_vectorizer.transform([kalimat])
            abusiveness_score = model.predict_proba(tfidf_text)[0]
            output.write(f"Kalimat: {kalimat}\n")
            output.write(f"Positif: {abusiveness_score[0]:.2f}, Negatif: {abusiveness_score[1]:.2f}\n\n")
