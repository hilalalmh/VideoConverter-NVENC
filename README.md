# VideoConverter-NVENC

Batch video converter berbasis Python dan FFmpeg dengan akselerasi GPU NVIDIA NVENC. Project ini dirancang untuk mengonversi berbagai format video ke MP4 secara otomatis dengan memanfaatkan hardware encoding pada GPU NVIDIA.

## ✨ Features

* 🎬 Convert video ke format MP4 secara otomatis
* 🚀 NVIDIA NVENC hardware encoding
* ⚡ Mendukung multiple conversion secara paralel
* 🖥️ GPU decoding menggunakan CUDA
* 🎞️ Mendukung berbagai format:

  * MKV
  * AVI
  * MOV
  * WMV
  * FLV
  * WEBM
  * TS
* 🔊 Audio dikonversi ke AAC 192 kbps
* 📺 Video menggunakan H.264
* 💾 Menggunakan output `yuv420p` untuk kompatibilitas luas
* ⏩ Otomatis melewati file yang sudah dikonversi
* 📊 Progress bar menggunakan `tqdm`
* 📁 Hasil konversi disimpan otomatis ke folder `convert`

## 🛠️ Requirements

### Software

* Python 3.9 atau lebih baru
* FFmpeg
* NVIDIA GPU dengan dukungan NVENC
* NVIDIA Driver terbaru

### Python Package

Install dependency dengan:

```bash
pip install -r requirements.txt
```

Atau:

```bash
pip install tqdm
```

## 🎮 NVIDIA GPU

Project ini menggunakan:

```text
h264_nvenc
```

sebagai hardware encoder NVIDIA.

GPU NVIDIA yang mendukung NVENC dapat digunakan. Performa dan jumlah proses paralel yang optimal bergantung pada GPU yang digunakan.

Contoh konfigurasi:

```python
MAX_WORKERS = 2
```

Untuk GPU kelas entry-level seperti GTX 1650 Ti, dua proses paralel dapat digunakan sebagai titik awal.

## 📦 Installation

### 1. Clone repository

```bash
git clone https://github.com/hilalalhm/VideoConverter-NVENC.git
```

Masuk ke folder:

```bash
cd VideoConverter-NVENC
```

### 2. Install Python dependency

```bash
pip install -r requirements.txt
```

### 3. Install FFmpeg

Pastikan FFmpeg sudah terinstall dan dapat dipanggil melalui terminal:

```bash
ffmpeg -version
```

Jika command tersebut menampilkan informasi versi FFmpeg, berarti FFmpeg sudah siap digunakan.

## 🚀 Usage

Letakkan file video yang ingin dikonversi di folder yang sama dengan script.

Contoh:

```text
VideoConverter-NVENC/
├── convert.py
├── requirements.txt
├── README.md
├── video1.mkv
├── video2.avi
└── video3.ts
```

Jalankan:

```bash
python convert.py
```

Program akan membuat folder:

```text
convert/
```

dan menyimpan hasil konversi di dalamnya:

```text
VideoConverter-NVENC/
├── convert.py
├── video1.mkv
├── video2.avi
├── convert/
│   ├── video1.mp4
│   └── video2.mp4
```

## ⚙️ Encoding Configuration

Konfigurasi utama menggunakan:

```text
Codec       : H.264 NVENC
Preset      : P5
Rate Control: VBR
CQ          : 19
Pixel Format: YUV420P
Audio       : AAC 192 kbps
Fast Start  : Enabled
```

Parameter kualitas dapat disesuaikan melalui:

```python
"-cq", "19",
```

Secara umum:

| CQ | Kualitas      | Ukuran      |
| -: | ------------- | ----------- |
| 17 | Sangat tinggi | Besar       |
| 19 | Tinggi        | Sedang      |
| 21 | Baik          | Lebih kecil |
| 23 | Cukup baik    | Kecil       |

Semakin kecil nilai CQ, semakin tinggi kualitas dan biasanya semakin besar ukuran file.

## 📂 Supported Input Formats

Saat ini format yang didukung:

```text
.mkv
.avi
.mov
.wmv
.flv
.webm
.ts
```

Output:

```text
.mp4
```

## 🔧 Customization

Jumlah proses paralel dapat diubah melalui:

```python
MAX_WORKERS = 2
```

Contoh:

```python
MAX_WORKERS = 1
```

untuk menjalankan satu proses FFmpeg pada satu waktu.

Atau:

```python
MAX_WORKERS = 2
```

untuk menjalankan dua proses secara paralel.

Jumlah worker yang optimal bergantung pada kemampuan GPU, CPU, VRAM, dan jenis video yang dikonversi.

## ⚠️ Troubleshooting

### FFmpeg tidak ditemukan

Jika muncul error seperti:

```text
'ffmpeg' is not recognized as an internal or external command
```

pastikan FFmpeg sudah terinstall dan folder `bin` FFmpeg sudah ditambahkan ke Windows PATH.

Tes dengan:

```bash
ffmpeg -version
```

### NVIDIA NVENC tidak tersedia

Tes encoder dengan:

```bash
ffmpeg -encoders | findstr nvenc
```

Jika tersedia, biasanya akan muncul:

```text
h264_nvenc
hevc_nvenc
```

Pastikan NVIDIA Driver sudah terinstall dengan benar.

### Video gagal dikonversi

Beberapa video dapat gagal dikonversi karena:

* File rusak
* Codec tidak kompatibel
* Timestamp bermasalah
* Stream video tidak valid
* Audio bermasalah
* File memiliki struktur container yang tidak standar

Coba jalankan FFmpeg secara manual untuk melihat pesan error secara lengkap.

## 📜 License

Project ini dibuat untuk penggunaan pribadi, pembelajaran, dan pengembangan lebih lanjut.

Silakan modifikasi dan kembangkan sesuai kebutuhan.

---

## 👨‍💻 Author

**Hilal Al Hamdi**

GitHub:
https://github.com/hilalalhm

## ⭐ Support

Jika project ini bermanfaat, jangan lupa memberikan ⭐ pada repository.
