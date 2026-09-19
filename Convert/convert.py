import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
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
KEEP_SUBTITLES = True
KEEP_CHAPTERS = True
MAP_ALL_AUDIO = True  # False = hanya track audio pertama
SCAN_RECURSIVE = False

# =============================
# CONVERT FUNCTION
# =============================

def check_ffmpeg_available():
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=10,
        )
        return result.returncode == 0
    except Exception:
        return False


def convert_to_mp4_gpu(input_path, output_path):
    filename = os.path.basename(input_path)

    if os.path.exists(output_path):
        return f"⏩ Skip: {filename}"

    part_path = output_path + ".part"

    command = [
        "ffmpeg",
        "-y",
        "-nostdin",

        # ===== penting untuk TS =====
        "-fflags", "+genpts",
        "-avoid_negative_ts", "make_zero",

        # ===== GPU decoding =====
        "-hwaccel", "cuda",

        "-i", input_path,

        # ===== mapping stream =====
        "-map_metadata", "0",
        "-map", "0:v:0",
    ]

    if MAP_ALL_AUDIO:
        command.extend(["-map", "0:a?"])
    else:
        command.extend(["-map", "0:a:0?"])

    if KEEP_SUBTITLES:
        command.extend(["-map", "0:s?"])

    if KEEP_CHAPTERS:
        command.extend(["-map_chapters", "0"])

    command.extend([

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
    ])

    if KEEP_SUBTITLES:
        command.extend(["-c:s", "mov_text"])

    command.append(part_path)

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            timeout=7200,
        )

    except subprocess.TimeoutExpired:
        try:
            os.remove(part_path)
        except OSError:
            pass

        return f"⏰ Timeout: {filename}"

    if result.returncode != 0:
        try:
            error_log = output_path + ".error.txt"

            with open(error_log, "w", encoding="utf-8") as f:
                f.write(result.stderr or "")

        except OSError:
            pass

        try:
            os.remove(part_path)
        except OSError:
            pass

        return f"❌ Gagal: {filename} (log: {os.path.basename(error_log)})"

    os.replace(part_path, output_path)

    return f"✔ Converted: {filename}"

# =============================
# MAIN
# =============================

if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    if not check_ffmpeg_available():
        print("\n[ERROR] ffmpeg tidak ditemukan. Pastikan ffmpeg tersedia di PATH.")
        sys.exit(1)

    video_files = []

    output_abs = os.path.abspath(output_folder)

    if SCAN_RECURSIVE:
        for root, dirs, files in os.walk(source_folder):
            if os.path.abspath(root) == output_abs:
                continue

            dirs[:] = [
                d
                for d in dirs
                if os.path.abspath(os.path.join(root, d)) != output_abs
            ]

            for file in files:
                if file.lower().endswith(VIDEO_EXT):
                    full_path = os.path.join(root, file)
                    if os.path.isfile(full_path):
                        video_files.append(full_path)

    else:
        for file in os.listdir(source_folder):
            if file == "convert":
                continue

            if file.lower().endswith(VIDEO_EXT):
                full_path = os.path.join(source_folder, file)
                if os.path.isfile(full_path):
                    video_files.append(full_path)

    print(f"\n🔥 Total video ditemukan: {len(video_files)}\n")

    # Rencanakan nama output unik agar a.mkv & a.avi
    # tidak sama-sama menulis ke a.mp4.
    used_names = set()
    output_map = {}

    for f in video_files:
        name = os.path.splitext(os.path.basename(f))[0]

        candidate = name
        counter = 1

        while candidate in used_names:
            candidate = f"{name}_{counter}"
            counter += 1

        used_names.add(candidate)
        output_map[f] = os.path.join(
            output_folder,
            candidate + ".mp4",
        )

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [
            executor.submit(
                convert_to_mp4_gpu,
                f,
                output_map[f],
            )
            for f in video_files
        ]

        for future in tqdm(
            as_completed(futures),
            total=len(futures),
            desc="Converting",
            unit="video"
        ):
            print(future.result())

    print("\n🎉 Semua proses selesai!")