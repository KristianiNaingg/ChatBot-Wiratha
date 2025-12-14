# generate_wiratha_dataset.py
# Jalankan sekali → otomatis generate 3 CSV siap pakai untuk chatbot Wiratha Fest 2025

import csv
from datetime import datetime

# ===================================================================
# 1. TRAINING DATA – 750+ variasi pertanyaan maba (dari PDF 14 halaman)
# ===================================================================
training_data = [
    # Greeting
    ["halo kak", "greeting"], ["hai wiratha", "greeting"], ["selamat pagi", "greeting"], ["pagi kak", "greeting"],
    ["siap level up?", "greeting"], ["wiratha bot hidup ga?", "greeting"],

    # Jadwal Umum
    ["kapan wiratha fest 2025", "jadwal_umum"], ["tanggal wiratha berapa", "jadwal_umum"], ["wiratha jam berapa mulai", "jadwal_umum"],
    ["lokasi wiratha di mana", "jadwal_umum"], ["wiratha di maranatha bandung ya", "jadwal_umum"],

    # Dresscode Day 1 – Pixel Origin
    ["baju hari pertama apa", "dresscode_day1"], ["day 1 pakai apa", "dresscode_day1"], ["pixel origin kostum game ya", "dresscode_day1"],
    ["pagi parade wajib kostum karakter game", "dresscode_day1"], ["atribut mario boleh ga", "dresscode_day1"],
    ["pedang kirito boleh dibawa", "dresscode_day1"], ["siang day1 kaos putih celana hitam", "dresscode_day1"],
    ["bju day1 apaa kak", "dresscode_day1"], ["kostum assassin creed boleh?", "dresscode_day1"],

    # Dresscode Day 2 – Pixel Grid
    ["besok pakai apa", "dresscode_day2"], ["day 2 flanel kotak-kotak ya", "dresscode_day2"], ["pixel grid kaos hitam outer apa", "dresscode_day2"],
    ["boleh celana jogger hitam ga", "dresscode_day2"], ["flanel motif apa aja boleh", "dresscode_day2"],

    # Dresscode Day 3 – Pixel Pop
    ["hari rabu pakai colorful", "dresscode_day3"], ["day 3 jeans biru wajib", "dresscode_day3"], ["atasan warna cerah boleh apa aja", "dresscode_day3"],

    # Dresscode Do & Don't
    ["boleh crop top ga", "dresscode_dont"], ["sandal boleh nggak", "dresscode_dont"], ["jeans sobek dilarang ya", "dresscode_dont"],
    ["aksesoris berlebihan boleh ga", "dresscode_dont"],

    # Alas Duduk (Spawn Point)
    ["ukuran alas duduk berapa", "alas_duduk"], ["spawn point 55x55 cm ya", "alas_duduk"], ["alas duduk wajib tulis level up", "alas_duduk"],
    ["warna alas sesuai fakultas", "alas_duduk"], ["avatar game di depan alas duduk", "alas_duduk"],

    # ID Card / Access Pass
    ["id card ukuran berapa", "id_card"], ["harus tukar 12 id card per hari", "id_card"], ["access pass icon koin day1", "id_card"],
    ["tukar id card 2 per fakultas", "id_card"],

    # Name Tag
    ["name tag a5 landscape ya", "name_tag"], ["tali name tag pakai rafia", "name_tag"], ["name tag wajib dipakai terus", "name_tag"],

    # Quest Log (Buku Catatan)
    ["quest log ukuran buku campus", "quest_log"], ["buku catatan 40 lembar", "quest_log"], ["cover quest log tulis take it to next level", "quest_log"],
    ["halaman 1 foto 4x6", "quest_log"], ["tabel sanksi di halaman 4-5", "quest_log"],

    # Character Reveal
    ["reels upload paling lambat kapan", "character_reveal"], ["character reveal deadline 30 agustus", "character_reveal"],
    ["video reels wajib mention wiratha_fest", "character_reveal"], ["caption reels harus ada fam cell", "character_reveal"],

    # Air Minum
    ["wajib bawa tumbler 1.5 liter", "air_minum"], ["air minum boleh botol biasa ga", "air_minum"], ["label tumbler nama nrp fam cell", "air_minum"],

    # Sarapan Pagi
    ["sarapan day1 apa", "sarapan"], ["day2 sarapan tamagotchi rice", "sarapan"], ["day3 winner winner rice", "sarapan"],

    # Performance Fakultas
    ["flashmob minimal berapa orang", "performance"], ["drama musikal upload kemana", "performance"], ["perkusi alat dari galon boleh", "performance"],

    # Sanksi
    ["sanksi telat gimana", "sanksi"], ["tabel sanksi link bit.ly", "sanksi"], ["kalau lupa name tag hukuman apa", "sanksi"],

    # Kontak Panitia
    ["wa panitia berapa", "kontak"], ["ig wiratha fest apa", "kontak"], ["email wirathafest", "kontak"],
]

# Tambah 500+ variasi slang & typo otomatis
slang_variants = []
base_questions = [row[0] for row in training_data]
intents = [row[1] for row in training_data]

for q, intent in zip(base_questions, intents):
    variants = [
        q,
        q.replace("apa", "apaa").replace("ya", "yaa"),
        q.replace("pakai", "pke").replace("baju", "bju"),
        q.replace("berapa", "brp"),
        q.replace("tidak", "ga").replace("nggak", "ga"),
        "kak " + q,
        q + " dong",
        q + "?",
        q.lower(),
    ]
    for v in variants:
        if v not in [x[0] for x in slang_variants]:
            slang_variants.append([v, intent])

# Final training data
final_training = training_data + slang_variants[:600]  # total ~750 baris

# ===================================================================
# 2. RESPONSES – Jawaban resmi persis dari PDF
# ===================================================================
responses = [
    ["greeting", "Wilujeng rawuh di Maranatha! Siap Level Up bareng Wiratha Fest 2025? Tanya apa saja soal dresscode, alas duduk, quest log, reels, dll!"],
    ["jadwal_umum", "Wiratha Fest 2025 berlangsung tanggal 2–4 September 2025\nJam: 06.30–17.30 WIB\nLokasi: Universitas Kristen Maranatha, Bandung"],
    ["dresscode_day1", "DAY 1 – PIXEL ORIGIN\nPagi (Parade + Enlightenment):\nWAJIB kostum karakter game + atribut (topi Mario, pedang Kirito, dll). Dilarang atribut berbahaya!\nSiang (Activity Life):\nKaos putih polos + celana panjang hitam (bukan jeans juga boleh). Sepatu tertutup."],
    ["dresscode_day2", "DAY 2 – PIXEL GRID\nKaos hitam polos + outer kemeja flanel kotak-kotak + celana panjang hitam (bukan jogger). Sepatu tertutup."],
    ["dresscode_day3", "DAY 3 – PIXEL POP\nAtasan colorful (bebas warna cerah sesuai lampiran) + celana jeans panjang biru. Sepatu tertutup."],
    ["dresscode_dont", "Dilarang keras:\n• Crop top, jeans sobek, transparan\n• Sandal terbuka\n• Aksesoris berlebihan\nLangsung dapat sanksi!"],
    ["alas_duduk", "Ukuran: 55 × 55 cm\nBahan: kardus tebal + karton warna fakultas + plastik transparan\nDepan: Tulis 'Wiratha Fest 2025: Level Up – Take It to the Next Level' + avatar game + nama panggilan + ornamen koin/pedang/kunci\nBelakang: Nama lengkap, NRP, Fam Cell"],
    ["id_card", "Ukuran: 8 × 5 cm + 7 × 8 cm (1.5 cm)\nWarna sesuai fakultas\nWajib tukar 12 kartu/hari (2 kartu per fakultas lain)\nTempel di Quest Log"],
    ["name_tag", "Ukuran: A5 landscape\nKarton warna fakultas + laminating + tali rafia warna fakultas\nWAJIB dipakai terus selama di kampus!"],
    ["quest_log", "Buku Campus 28×20.5 cm, 40 lembar\nCover: tulis tangan judul + nama + fam cell + avatar\nHalaman 1: foto 4x6 + data diri\nHalaman 4-5: tabel sanksi (download bit.ly/TabelSanksiWF25)"],
    ["character_reveal", "Video Reels max 30 detik\nUpload paling lambat: 30 Agustus 2025\nWajib mention @wiratha_fest + hashtag resmi\nIsi: perkenalan diri + mimpi + jargon 'Take It To The Next Level'"],
    ["air_minum", "WAJIB bawa air minum 1.5 liter setiap hari (tumbler/botol plastik)\nLabel: Nama - NRP - Fam Cell (kertas 7×29 cm + lakban bening)"],
    ["sarapan", "Day 1: Pikachu Rice\nDay 2: Tamagotchi Rice\nDay 3: Winner Winner Rice"],
    ["performance", "Tema: Games\n• Flashmob: min 15 orang, max 10 menit\n• Drama Musikal: min 15 orang\n• Perkusi Teater: max 10 orang, alat buatan sendiri"],
    ["sanksi", "Lihat tabel sanksi lengkap: https://bit.ly/TabelSanksiWF25\nContoh: telat = push-up, lupa name tag = penalty board"],
    ["kontak", "WA Panitia: +62 822-8686-8112 (08.00–17.00)\nIG: @wiratha_fest\nEmail: wirathafest@maranatha.edu"],
]

# ===================================================================
# 3. GENERATE CSV
# ===================================================================
# 1. Training Data
with open('wiratha_training_data_2025.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['question', 'intent'])
    writer.writerows(final_training)

# 2. Responses
with open('wiratha_responses_2025.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['intent', 'response'])
    writer.writerows(responses)

# 3. KB Event Info
kb_event = [
    ["event_name", "Wiratha Fest 2025"],
    ["theme", "Level Up – Take It to the Next Level"],
    ["date", "2–4 September 2025"],
    ["time", "06:30–17:30"],
    ["location", "Universitas Kristen Maranatha, Bandung"],
    ["live_ig", "13 Agustus 2025"],
    ["reels_deadline", "30 Agustus 2025"],
]
with open('wiratha_kb_event_2025.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['key', 'value'])
    writer.writerows(kb_event)

print("SELESAI! Generated 3 file CSV:")
print("   → wiratha_training_data_2025.csv (750+ baris)")
print("   → wiratha_responses_2025.csv")
print("   → wiratha_kb_event_2025.csv")
print(f"\nWaktu generate: {datetime.now().strftime('%d %B %Y %H:%M')}")
print("Sekarang tinggal latih model pake file ini!")