import joblib
import pandas as pd
import re

# Load model dan data respon
try:
    model = joblib.load('wiratha_model_final.pkl')
    responses_df = pd.read_csv('wiratha_responses_2025.csv')
    print("✅ Model dan Database berhasil dimuat.\n")
except Exception as e:
    print(f"❌ Error: {e}")
    exit()

def preprocess_wiratha(text):
    if not text or not isinstance(text, str): return ""
    text = text.lower().strip()
    slang = {
        "ga":"tidak", "gak":"tidak", "pke":"pakai", "bju":"baju",
        "brp":"berapa", "dmn":"dimana", "sy":"saya", "wf":"wiratha fest"
    }
    for k, v in slang.items():
        text = re.sub(rf'\b{k}\b', v, text)
    text = re.sub(r'[^\w\s\?]', ' ', text)
    return text

# Daftar skenario pengujian
test_cases = [
    "Halo kak, semangat pagi!",
    "kapan wiratha fest 2025 dimulai?",
    "kak bju day1 apaa??",
    "sarapan hari pertama apa kak?",
    "ukuran alas duduk berapa?",
    "sy lupa bawa nametag kena sanksi apa?",
    "boleh pke sandal ga?",
    "makan bang" # Tes untuk melihat fallback (confidence rendah)
]

print(f"{'INPUT':<35} | {'INTENT':<15} | {'PREDICTION'}")
print("-" * 80)

for query in test_cases:
    cleaned = preprocess_wiratha(query)
    
    # Dapatkan probabilitas
    probs = model.predict_proba([cleaned])[0]
    max_prob = max(probs)
    intent = model.classes_[probs.argmax()]
    
    # Logika fallback sederhana untuk testing
    if max_prob < 0.45:
        intent = "fallback"
        
    print(f"{query:<35} | {intent:<15} | {max_prob:.2%}")