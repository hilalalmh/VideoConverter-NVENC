import os
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import freeze_support
from tqdm import tqdm

# =============================
# CONFIG
# =============================

script_dir = os.path.dirname(os.path.abspath(__file__))
source_folder = script_dir
output_folder = os.path.join(source_folder, "convert")
os.makedirs(output_folder, exist_ok=True)

VIDEO_EXT = (".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".ts")
MAX_WORKERS = 2  # GTX 1650 Ti aman 2 proses NVENC

# =============================
# CONVERT FUNCTION
# =============================

def convert_to_mp4_gpu(input_path):
    filename = os.path.basename(input_path)
    name, ext = os.path.splitext(filename)
    output_path = os.path.join(output_folder, name + ".mp4")

    if os.path.exists(output_path):
        return f"⏩ Skip: {filename}"

    command = [
        "ffmpeg",
        "-y",

        # ===== penting untuk TS =====
        "-fflags", "+genpts",
        "-avoid_negative_ts", "make_zero",

        # ===== GPU decoding =====
        "-hwaccel", "cuda",

        "-i", input_path,

        # ===== mapping stream =====
        "-map_metadata", "0",
        "-map", "0:v:0",
        "-map", "0:a?",

        # ===== GPU encoding =====
        "-c:v", "h264_nvenc",
        "-preset", "p5",
        "-rc", "vbr",
        "-cq", "19",
        "-b:v", "0",

        # ===== kompatibilitas =====
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",

        # ===== audio =====
        "-c:a", "aac",
        "-b:a", "192k",

        output_path
    ]

    try:
        subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return f"✔ Converted: {filename}"
    except subprocess.CalledProcessError:
        return f"❌ Gagal: {filename}"

# =============================
# MAIN
# =============================

if __name__ == "__main__":
    freeze_support()

    video_files = []

    for file in os.listdir(source_folder):
        if file == "convert":
            continue

        if file.lower().endswith(VIDEO_EXT):
            full_path = os.path.join(source_folder, file)
            if os.path.isfile(full_path):
                video_files.append(full_path)

    print(f"\n🔥 Total video ditemukan: {len(video_files)}\n")

    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(convert_to_mp4_gpu, f) for f in video_files]

        for future in tqdm(
            as_completed(futures),
            total=len(futures),
            desc="Converting",
            unit="video"
        ):
            print(future.result())

    print("\n🎉 Semua proses selesai!")