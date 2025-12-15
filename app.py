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
        # Slang Maranatha & Singkatan Umum
        
        # Negasi/Kata Umum
        "ga":"tidak", "gak":"tidak", "gk":"tidak", "nggak":"tidak", "ngga":"tidak",
        "brp":"berapa", "smpe":"sampai", "bsok":"besok", "bsk":"besok",
        "pke":"pakai", "pake":"pakai", "apaa":"apa", "yaa":"ya",
        "kpn":"kapan", "dmana":"dimana", "dmn":"dimana", "sana":"disana", 
        "sy":"saya", "gw":"saya", "ane":"saya", "ak":"saya",
        "org":"orang", "ktmu":"ketemu", "kyk":"kayak", "gni":"begini", "gitu":"begitu",
        "jd":"jadi", "tdk":"tidak",
        
        # Perlengkapan / Dress Code
        "bju":"baju", "bajuu":"baju", "bajuuuu":"baju",
        "drsscode":"dress code", "dresscode":"dress code", "drescode":"dress code",
        "kmeja":"kemeja", "kemejaaa":"kemeja", "kemejaa":"kemeja",
        "celana":"celana", "clana":"celana", "cnlna":"celana",
        "joger":"jogger", "flanel":"flanel", "kaos":"kaos", "kaoss":"kaos", "kats":"kaus",
        "ktk":"kotak", "kotakkotak":"kotak-kotak",
        "alasduduk":"alas duduk", "alas dudk":"alas duduk", "spawnpoint":"alas duduk", "spawn":"alas duduk",
        "tumbler":"tumbler", "tummblr":"tumbler", "botol":"botol minum", "botolminum":"botol minum",
        
        # Identitas / Atribut
        "idcard":"id card", "accesspass":"id card", "namtag":"name tag", "nametag":"name tag",
        "nim":"nomor induk mahasiswa", "npm":"nomor pokok mahasiswa",
        "reels":"character reveal", "charreveal":"character reveal",
        "fcm":"fam cell",
        
        # Acara / Lokasi
        "wf":"wiratha fest", "maba":"mahasiswa baru", "famcell":"fam cell",
        "regis":"registrasi", "regist":"registrasi", "regitrasi":"registrasi",
        "loc":"lokasi", "tempat":"tempat", "tmpt":"tempat",
        "jam":"jam", "mulai":"mulai", "selesai":"selesai",
        "panitia":"panitia", "kakak":"panitia", "kak":"panitia"
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
