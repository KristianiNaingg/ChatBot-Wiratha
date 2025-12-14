# app.py
from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import re

app = Flask(__name__)

# Load model & data
model = joblib.load('wiratha_model_final.pkl')
responses_df = pd.read_csv('wiratha_responses_2025.csv')

# === PREPROCESSING SUPER KUAT (Versi Final dari PDF Resmi) ===
def preprocess_wiratha(text):
    if not text or not isinstance(text, str):
        return ""
    text = text.lower().strip()
    
    slang = {
        # Slang maba Maranatha 2025
        "ga":"tidak", "gak":"tidak", "gk":"tidak", "nggak":"tidak", "ngga":"tidak",
        "bju":"baju", "bajuu":"baju", "bajuuuu":"baju",
        "drsscode":"dress code", "dresscode":"dress code", "drescode":"dress code",
        "alasduduk":"alas duduk", "alas dudk":"alas duduk", "spawnpoint":"alas duduk", "spawn":"alas duduk",
        "idcard":"id card", "accesspass":"id card", "namtag":"name tag", "nametag":"name tag",
        "reels":"character reveal", "charreveal":"character reveal",
        "tumbler":"tumbler", "flanel":"flanel", "kmeja":"kemeja", "joger":"jogger",
        "wf":"wiratha fest", "maba":"mahasiswa baru", "famcell":"fam cell",
        "brp":"berapa", "smpe":"sampai", "bsok":"besok", "bsk":"besok",
        "pke":"pakai", "pake":"pakai", "apaa":"apa", "yaa":"ya"
    }
    
    for k, v in slang.items():
        text = re.sub(rf'\b{k}\b', v, text)
    text = re.sub(r'[^\w\s\?]', ' ', text)
    text = re.sub(r'(.)\1{2,}', r'\1\1', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message', '').strip()
    if not user_msg:
        return jsonify({'reply': 'Maaf, pesan kosong ya'})
    
    cleaned = preprocess_wiratha(user_msg)
    if not cleaned:
        return jsonify({'reply': responses_df[responses_df['intent'] == 'fallback']['response'].iloc[0]})
    
    predicted_intent = model.predict([cleaned])[0]
    
    # Fallback jika intent tidak ditemukan
    response = responses_df[responses_df['intent'] == predicted_intent]['response']
    if response.empty:
        response = responses_df[responses_df['intent'] == 'fallback']['response']
    
    return jsonify({'reply': response.iloc[0]})

if __name__ == '__main__':
    app.run(debug=True)