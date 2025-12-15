// app.js
document.addEventListener('DOMContentLoaded', () => {
    const chatWindow = document.getElementById('chat-window');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    
    // Alamat API Backend Flask disesuaikan dengan app.py: menggunakan route '/chat'
    const API_URL = '/chat'; 

    // --- UTILITY FUNCTIONS ---

    // Fungsi untuk menggulir chatbox ke bawah
    const scrollToBottom = () => {
        chatWindow.scrollTop = chatWindow.scrollHeight;
    };

    // Fungsi untuk Menambahkan Pesan ke UI
    const appendMessage = (message, sender) => {
        // 1. Buat Wrapper Baris (Message Row)
        const rowElement = document.createElement('div');
        rowElement.classList.add('message-row', sender);

        // 2. Buat Bubble Chat
        const bubbleElement = document.createElement('div');
        bubbleElement.classList.add('chat-bubble', sender);
        // Menggunakan innerHTML agar bisa render tag HTML (misal: <b> atau list)
        bubbleElement.innerHTML = message.replace(/\n/g, '<br>');

        // 3. Susun Elemen (Koreksi Logika Fatal)
        if (sender === 'bot') {
            const avatarElement = document.createElement('div'); 
            avatarElement.classList.add('avatar');
            avatarElement.innerHTML = '<i class="fa-solid fa-robot"></i>';
            
            // Urutan BOT: Avatar | Bubble
            rowElement.appendChild(avatarElement); // Tambahkan Avatar
            rowElement.appendChild(bubbleElement); // Tambahkan Bubble
        } else {
            // Urutan USER: Hanya Bubble
            rowElement.appendChild(bubbleElement);
        }
        
        // Masukkan ke Chat Window
        chatWindow.appendChild(rowElement);
        // Auto-scroll ke bawah
        scrollToBottom();
    };


    // --- MAIN FUNCTION ---

    // Fungsi untuk mengirim pesan
    const sendMessage = async () => {
        const userMessage = userInput.value.trim();
        if (userMessage === '') return;

        // 1. Tampilkan pesan user di chat window
        appendMessage(userMessage, 'user');
        
        // Kosongkan input dan nonaktifkan UI saat loading
        userInput.value = '';
        userInput.disabled = true; 
        sendBtn.disabled = true;

        try {
            // 2. Kirim pesan user ke API Backend
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                // Mengirim data dengan kunci 'message'
                body: JSON.stringify({ message: userMessage }), 
            });

            if (!response.ok) {
                // Tangani non-200 status (misal: 500 Internal Server Error)
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            // Menerima balasan dari 'reply', sesuai dengan output app.py
            const botMessage = data.reply; 

            // 3. Tampilkan jawaban bot di chat window
            setTimeout(() => {
                appendMessage(botMessage, 'bot');
            }, 300); // Penundaan agar terlihat natural

        } catch (error) {
            console.error('Error:', error);
            const errorMessage = 'Maaf, terjadi masalah koneksi ke server atau error internal.';
            setTimeout(() => {
                appendMessage(errorMessage, 'bot');
            }, 300);
        } finally {
            // Aktifkan kembali input dan tombol
            userInput.disabled = false;
            sendBtn.disabled = false;
            userInput.focus(); 
        }
    };

    // --- EVENT LISTENERS ---
    
    // 1. Event Listener untuk tombol Kirim (klik)
    sendBtn.addEventListener('click', sendMessage);

    // 2. Event Listener untuk tombol Enter
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault(); // Mencegah form submission atau newline
            sendMessage();
        }
    });

    // Gulir ke bawah saat halaman dimuat (untuk melihat pesan sapaan awal)
    scrollToBottom();
});