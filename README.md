<div class = "center">
    <img src = "./html-to-exe/icon.ico"
</div>

# Jika menggunakan Python
**pip install html-to-exe** 
 
`` html-to-exe ``


# Jika menggunakan Node.js
**npm install -g html-to-exe**

`` node bin/html-to-exe.js ``

**Aplikasi Konversi Proyek Web ke Desktop dengan Electron**  

<img src = "html.gif" width ="auto" height = "auto">

<a href = "https://pypi.org/project/html-to-exe/">Open Project PYPI Python Licensi</a>

---

## **📋 Daftar Isi**  
1. [Deskripsi Proyek](#-deskripsi-proyek)  
2. [Fitur Utama](#-fitur-utama)  
3. [Algoritma & Arsitektur](#-algoritma--arsitektur)  
4. [Persyaratan Sistem](#-persyaratan-sistem)  
5. [Panduan Instalasi Lengkap](#-panduan-instalasi-lengkap)  
6. [Cara Penggunaan](#-cara-penggunaan)  
7. [Troubleshooting](#-troubleshooting)  
8. [Kontribusi](#-kontribusi)  
9. [Lisensi](#-lisensi)  

---

## **📌 Deskripsi Proyek**  
Aplikasi **HTML to EXE Converter** memungkinkan pengguna mengubah proyek web (HTML, CSS, JavaScript) menjadi aplikasi desktop berbasis **Electron** yang dapat dijalankan di **Windows, macOS, dan Linux**.  

🔹 **Mengapa menggunakan aplikasi ini?**  
✔ Mudah digunakan dengan antarmuka GUI (Graphical User Interface)  
✔ Mendukung berbagai konfigurasi window (ukuran, fullscreen, frameless, dll.)  
✔ Preview langsung sebelum konversi  
✔ Dapat menambahkan ikon aplikasi khusus  

---

## **✨ Fitur Utama**  
✅ **Konversi ke EXE**  
- Mendukung **Windows (.exe), macOS (.app), Linux (binary)**  
- Opsi **pengemasan dengan ASAR** (enkripsi file sumber)  

✅ **Konfigurasi Window**  
- Ukuran (width, height, min/max dimensions)  
- Mode **Fullscreen & Kiosk**  
- **Warna latar belakang** dan transparansi  
- **Frame window** (borders, title bar)  

✅ **Web Preferences**  
- **Node.js Integration** (akses filesystem dari JavaScript)  
- **Context Isolation** (keamanan tambahan)  
- **WebGL & Sandbox Mode**  

✅ **Preview Mode**  
- **Server lokal** untuk melihat hasil sebelum konversi  
- Buka di **browser** atau **Electron window**  

✅ **Logging & Error Handling**  
- Output log detail selama proses konversi  
- Pengecekan otomatis **Node.js & Electron**  

---

## **⚙ Algoritma & Arsitektur**  

### **📂 Alur Kerja Utama**  
```mermaid
graph TD
    A[Start] --> B[Pilih Folder HTML]
    B --> C[Konfigurasi Aplikasi]
    C --> D[Generate main.js & package.json]
    D --> E[NPM Install Dependencies]
    E --> F[Electron-Packager Build]
    F --> G[Output EXE]
    G --> H[Selesai]
```

### **🔧 Proses Konversi**  
1. **Input:**  
   - Folder HTML (`index.html` harus ada)  
   - Nama aplikasi, output directory, ikon (opsional)  

2. **Generate Project Electron:**  
   - Buat `package.json` dengan konfigurasi dasar  
   - Generate `main.js` berdasarkan pengaturan GUI  

3. **Proses Build:**  
   - Jalankan `npm install` untuk menginstal Electron  
   - Gunakan `electron-packager` untuk membuat executable  

4. **Output:**  
   - File aplikasi siap pakai di folder `dist/`  

---

## **🖥 Persyaratan Sistem**  
| Komponen | Versi Minimal | Catatan |
|----------|--------------|---------|
| **OS** | Windows 10 / macOS 10.12+ / Linux (x64) | - |
| **Python** | 3.6+ | Untuk menjalankan GUI |
| **Node.js** | 14.x+ | Wajib untuk Electron |
| **npm** | 6.x+ | Package manager Node.js |
| **RAM** | 2GB+ | Lebih baik 4GB untuk build besar |

---
## **📥 Panduan Instalasi Terminal**

 ```bash
pip install html-to-exe
html-to-exe
  ```

## **📥 Panduan Instalasi Lengkap**  

### **1️⃣ Instal Python & PIP**  
- Download Python dari [python.org](https://www.python.org/downloads/)  
- Pastikan **"Add Python to PATH"** dicentang saat instalasi  
- Verifikasi instalasi:  
  ```bash
  python --version
  pip --version
  ```

### **2️⃣ Instal Node.js & npm**  
- Download dari [nodejs.org](https://nodejs.org/) (pilih **LTS version**)  
- Verifikasi instalasi:  
  ```bash
  node --version
  npm --version
  ```

### **3️⃣ Clone/Download Proyek**  
```bash
git clone https://github.com/username/html-to-exe-converter.git
cd html-to-exe
```

### **4️⃣ Instal Dependencies Python**  
```bash
pip install tk pillow
```

### **5️⃣ Jalankan Aplikasi**  
```bash
python gui.py
```
**Atau buat EXE untuk GUI ini sendiri:**  
```bash
pyinstaller --onefile --windowed --icon=icon.ico gui.py
```

---

## **🖱 Cara Penggunaan**  

### **1️⃣ Tab Settings**  
- **HTML Folder**: Pilih folder yang berisi `index.html`  
- **App Name**: Nama aplikasi output  
- **Output Folder**: Lokasi penyimpanan hasil konversi  
- **Icon (Opsional)**: `.ico` (Windows), `.icns` (macOS), `.png` (Linux)  
- **Platform**: Pilih OS target  

### **2️⃣ Tab Electron Options**  
- **Window Settings**: Ukuran, resizable, fullscreen  
- **Web Preferences**: Node.js integration, sandbox mode  

### **3️⃣ Tab Preview**  
- **Start Preview**: Jalankan pratinjau di Electron  
- **Open in Browser**: Buka di browser default  

### **4️⃣ Konversi ke EXE**  
- Klik **"Convert to EXE"**  
- Proses akan berjalan, lihat log di **Output Console**  

---

## **⚠ Troubleshooting**  

| Masalah | Solusi |
|---------|--------|
| **Node.js tidak terdeteksi** | Pastikan Node.js terinstall dan PATH benar |
| **Error saat konversi** | Periksa log, pastikan `index.html` ada |
| **Preview tidak muncul** | Tutup aplikasi lain yang menggunakan port yang sama |
| **Build gagal** | Coba `npm install electron --global` |

---

## **🤝 Kontribusi**  
- **Laporkan bug** di [Issues](https://github.com/Royhtml/html-to-exe/issues)  
- **Ajukan fitur baru** via Pull Request  

---

## **📜 Lisensi**  
**MIT License** - Bebas digunakan untuk proyek komersial & open source.  

---
**🎉 Selamat Mencoba!** 🚀
