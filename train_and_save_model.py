import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import joblib

# Baca data training
df = pd.read_csv('wiratha_training_data_2025.csv')

X = df['question']
y = df['intent']

# Penyesuaian: Menggunakan sublinear_tf agar kata yang muncul sangat sering 
# tidak mendominasi secara ekstrem
model = make_pipeline(
    TfidfVectorizer(ngram_range=(1,3), sublinear_tf=True), 
    MultinomialNB(alpha=0.1) # Alpha rendah agar lebih sensitif pada kata kunci unik
)

model.fit(X, y)

# Simpan model baru
joblib.dump(model, 'wiratha_model_final.pkl')
print("Model berhasil diperbarui dengan sistem probabilitas!")