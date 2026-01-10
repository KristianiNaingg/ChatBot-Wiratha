import csv

# Konfigurasi Intent Tambahan (Sanksi & Atribut)
dataset_config = {
    "sanksi": {
        "keywords": ["sanksi", "hukuman", "pelanggaran", "denda", "penalty", "konsekuensi"],
        "context": ["telat", "lupa nametag", "atribut kurang", "tidak bawa tumbler", "salah baju"],
    },
    "id_card": {
        "keywords": ["id card", "access pass", "tukar kartu", "kartu fakultas", "namtag"],
        "context": ["ukuran", "berapa buah", "tukar dimana", "warna apa", "rafia"],
    },
    "jadwal_umum": {
        "keywords": ["kapan", "jam berapa", "lokasi", "tempat", "tanggal"],
        "context": ["mulai", "selesai", "wiratha fest", "maranatha", "bandung"],
    }
}

templates = [
    "{keyword} {context} gimana?",
    "kalo {context} {keyword} nya apa kak?",
    "info dong buat {keyword} {context}",
    "kak mau nanya tentang {keyword} {context}",
    "{context} itu {keyword} nya gimana ya?",
    "spill {keyword} {context} dong panitia",
    "{keyword} {context}",
]

def generate_shotgun_v2():
    new_data = []
    
    for intent, config in dataset_config.items():
        for kw in config["keywords"]:
            for ctx in config["context"]:
                for temp in templates:
                    # Generate variasi normal
                    question = temp.format(keyword=kw, context=ctx)
                    new_data.append([question, intent])
                    
                    # Tambahkan variasi singkat/slang
                    new_data.append([f"kak {question}", intent])
                    new_data.append([question.replace("gimana", "gmn").replace("apa", "ap"), intent])

    with open('wiratha_training_data_2025.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(new_data)
    
    print(f"✅ Shotgun Selesai! Menambahkan {len(new_data)} variasi sanksi, id card, dan jadwal.")

if __name__ == "__main__":
    generate_shotgun_v2()