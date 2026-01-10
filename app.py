from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import re
import numpy as np

app = Flask(__name__)

# Load model & data
model = joblib.load('wiratha_model_final.pkl')
responses_df = pd.read_csv('wiratha_responses_2025.csv')

def preprocess_wiratha(text):
    if not text or not isinstance(text, str):
        return ""
    
    text = text.lower().strip()
    
    # Kamus Slang yang diperluas
    slang = {
        "makanan": "sarapan",
        "makan": "sarapan",
        "bekal": "sarapan",
        "menu": "sarapan","ga":"tidak", "gak":"tidak", "gk":"tidak", "nggak":"tidak", "ngga":"tidak",
        "brp":"berapa", "smpe":"sampai", "bsok":"besok", "bsk":"besok",
        "pke":"pakai", "pake":"pakai", "sy":"saya", "gw":"saya", "ak":"saya",
        "org":"orang", "jd":"jadi", "tdk":"tidak", "udh":"sudah", "dah":"sudah",
        "bju":"baju", "drsscode":"dress code", "dresscode":"dress code",
        "idcard":"id card", "nametag":"name tag", "reels":"character reveal",
        "wf":"wiratha fest", "maba":"mahasiswa baru", "famcell":"fam cell",
        "regis":"registrasi", "loc":"lokasi", "tmpt":"tempat", "kak":"panitia"
    }
    
    # Normalisasi kata berdasarkan kamus
    for k, v in slang.items():
        text = re.sub(rf'\b{k}\b', v, text)
    
    # Hapus simbol tapi pertahankan tanda tanya untuk konteks
    text = re.sub(r'[^\w\s\?]', ' ', text)
    
    # Hapus huruf berulang (bajuuuuu -> baju)
    text = re.sub(r'(.)\1{2,}', r'\1\1', text)
    
    # Normalisasi spasi
    text = re.sub(r'\s+', ' ', text).strip()
    return text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message', '').strip()
    if not user_msg:
        return jsonify({'reply': 'Wah, pesannya kosong nih. Tanya apa saja dong!'})
    
    cleaned = preprocess_wiratha(user_msg)
    if not cleaned:
        return jsonify({'reply': responses_df[responses_df['intent'] == 'fallback']['response'].iloc[0]})
    
    # Prediksi dengan Confidence Score
    # Kita menggunakan predict_proba untuk melihat seberapa yakin modelnya
    probs = model.predict_proba([cleaned])[0]
    max_prob = np.max(probs)
    predicted_intent = model.classes_[np.argmax(probs)]
    
    # Threshold: Jika keyakinan model di bawah 45%, gunakan fallback
    # Ini mencegah chatbot menjawab "ngawur"
    if max_prob < 0.45:
        predicted_intent = 'fallback'
    
    response = responses_df[responses_df['intent'] == predicted_intent]['response']
    
    if response.empty:
        response = responses_df[responses_df['intent'] == 'fallback']['response']
    
    return jsonify({
        'reply': response.iloc[0],
        'intent': predicted_intent, # Opsional: untuk debugging
        'confidence': float(max_prob) # Opsional: untuk debugging
    })

if __name__ == '__main__':
    app.run(debug=True)