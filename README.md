# VideoConverter-NVENC

A Python and FFmpeg based batch video converter with NVIDIA NVENC GPU acceleration. This project automatically converts various video formats to MP4 using hardware encoding on NVIDIA GPUs.

## ✨ Features

* 🎬 Automatically convert videos to MP4
* 🚀 NVIDIA NVENC hardware encoding
* ⚡ Parallel conversion support
* 🖥️ GPU decoding using CUDA
* 🎞️ Support for multiple formats:

  * MKV
  * AVI
  * MOV
  * WMV
  * FLV
  * WEBM
  * TS
* 🔊 Audio converted to AAC 192 kbps (choose: all tracks or first track only)
* 📺 Video encoded with H.264
* 💾 `yuv420p` output for broad compatibility
* ⏩ Skips already converted files
* 📊 Progress bar powered by `tqdm`
* 📁 Results saved automatically to the `convert` folder
* 💬 Subtitles preserved (converted to `mov_text`)
* 📑 Chapters preserved
* 🔒 Safe output writing: encodes to a `.part` file, then renames on success
* 📝 Error log saved to a `*.error.txt` file on failed conversion
* 🧵 Parallel conversion using threads (lightweight, no extra Python processes)
* 📂 Optional recursive scan for subfolders (config)

## 🛠️ Requirements

### Software

* Python 3.9 or newer
* FFmpeg
* NVIDIA GPU with NVENC support
* Up-to-date NVIDIA Driver

### Python Package

Install the dependency with:

```bash
pip install -r requirements.txt
```

Or:

```bash
pip install tqdm
```

## 🎮 NVIDIA GPU

This project uses:

```text
h264_nvenc
```

as the NVIDIA hardware encoder.

Any NVIDIA GPU with NVENC support can be used. Optimal performance and the number of parallel processes depend on the GPU.

Example configuration:

```python
MAX_WORKERS = 2
```

For entry-level GPUs such as the GTX 1650 Ti, two parallel processes are a good starting point.

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/hilalalmh/VideoConverter-NVENC.git
```

Enter the folder:

```bash
cd VideoConverter-NVENC
```

### 2. Install the Python dependency

```bash
pip install -r requirements.txt
```

### 3. Install FFmpeg

Make sure FFmpeg is installed and callable from the terminal:

```bash
ffmpeg -version
```

If the command prints the FFmpeg version info, FFmpeg is ready to use.

## 🚀 Usage

Place the video files you want to convert in the same folder as the script.

Example:

```text
VideoConverter-NVENC/
├── convert.py
├── requirements.txt
├── README.md
├── video1.mkv
├── video2.avi
└── video3.ts
```

Run:

```bash
python convert.py
```

The program will create a folder:

```text
convert/
```

and store the converted files there:

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

Main encoding settings:

```text
Codec       : H.264 NVENC
Preset      : P5
Rate Control: VBR
CQ          : 19
Pixel Format: YUV420P
Audio       : AAC 192 kbps
Subtitle    : MOV_TEXT (when KEEP_SUBTITLES = True)
Chapter     : Preserved (when KEEP_CHAPTERS = True)
Fast Start  : Enabled
```

Quality can be adjusted through:

```python
"-cq", "19",
```

In general:

| CQ | Quality        | Size       |
| -: | -------------- | ---------- |
| 17 | Very high      | Large      |
| 19 | High           | Medium     |
| 21 | Good           | Smaller    |
| 23 | Fairly good    | Small      |

The lower the CQ value, the higher the quality and usually the larger the file size.

## 📂 Supported Input Formats

Supported input formats:

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

All settings are available in the `CONFIG` section of `convert.py`:

```python
MAX_WORKERS     = 2          # Number of parallel conversions (ffmpeg)
KEEP_SUBTITLES  = True       # Preserve subtitles (False to discard)
KEEP_CHAPTERS   = True       # Preserve chapters
MAP_ALL_AUDIO   = True       # True = all audio tracks, False = first track only
SCAN_RECURSIVE  = False      # True = also scan videos in subfolders
```

### MAX_WORKERS

Example:

```python
MAX_WORKERS = 1
```

runs a single FFmpeg process at a time.

Or:

```python
MAX_WORKERS = 2
```

runs two processes in parallel.

The optimal number of workers depends on the GPU, CPU, VRAM, and the type of videos being converted.

### SCAN_RECURSIVE

```text
False → only video files in the script's main folder
True  → video files in the main folder + all subfolders
```

The `convert/` folder is always skipped, both in normal and recursive mode.

### MAP_ALL_AUDIO

```text
True  → all audio tracks are converted to AAC 192 kbps
False → only the first audio track is converted
```

### KEEP_SUBTITLES

When `True`, text subtitles (SRT/ASS) are converted to `mov_text` for MP4 compatibility.

> **Note:** bitmap subtitles (PGS/DVD) cannot be converted to `mov_text`. If a video contains bitmap subtitles, set `KEEP_SUBTITLES = False` to avoid conversion failure.

## ⚠️ Troubleshooting

### FFmpeg not found

The script checks for FFmpeg at startup and stops with:

```text
[ERROR] ffmpeg tidak ditemukan. Pastikan ffmpeg tersedia di PATH.
```

If you see this message, make sure FFmpeg is installed and its `bin` folder is added to the Windows PATH.

Test with:

```bash
ffmpeg -version
```

### NVIDIA NVENC unavailable

Test the encoder with:

```bash
ffmpeg -encoders | findstr nvenc
```

If available, output normally includes:

```text
h264_nvenc
hevc_nvenc
```

Make sure the NVIDIA Driver is installed correctly.

### Video failed to convert

On failure, the script writes a log file next to the output:

```text
name.mp4.error.txt
```

The log contains the full FFmpeg error output.

Some videos may fail to convert because of:

* Corrupted files
* Incompatible codecs
* Broken timestamps
* Invalid video streams
* Problematic audio
* Bitmap subtitles (PGS/DVD) — see the `KEEP_SUBTITLES` section
* Non-standard container structure

Run FFmpeg manually to get the full error message.

### Conversion timeout

Each FFmpeg process has a 2-hour (7200 seconds) limit.

If a video takes longer or FFmpeg hangs, the process is cancelled and the incomplete `.part` file is cleaned up automatically.

## 📜 License

This project is made for personal use, learning, and further development.

Feel free to modify and improve it as needed.

---

## 👨‍💻 Author

**Hilal Al Hamdi**

GitHub:
https://github.com/hilalalhm

## ⭐ Support

If you find this project useful, don't forget to give it a ⭐ on the repository.