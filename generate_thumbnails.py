from pathlib import Path
import subprocess
import hashlib
import sys

# 프로젝트 루트 기준
BASE_DIR = Path(__file__).resolve().parent
VIDEO_DIR = BASE_DIR / "videos"
THUMB_DIR = BASE_DIR / "thumbnails"

VIDEO_EXTS = {".mp4", ".mkv", ".webm", ".mov", ".avi"}


def get_thumb_name(rel_video: str) -> str:
    return hashlib.md5(rel_video.encode("utf-8")).hexdigest() + ".jpg"


def make_thumbnail(video_path: Path, thumb_path: Path) -> bool:
    if thumb_path.exists():
        return True

    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(video_path),
        "-ss", "00:00:02",
        "-vframes", "1",
        "-vf", "scale=320:-1",
        "-q:v", "2",
        str(thumb_path)
    ]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            print(f"[FAIL] {video_path}")
            print(result.stderr.strip())
            return False

        if thumb_path.exists():
            print(f"[OK]   {video_path.name}")
            return True

        print(f"[FAIL] {video_path} -> thumbnail not created")
        return False

    except subprocess.TimeoutExpired:
        print(f"[TIMEOUT] {video_path}")
        return False
    except Exception as e:
        print(f"[ERROR] {video_path} -> {e}")
        return False


def main():
    VIDEO_DIR.mkdir(exist_ok=True)
    THUMB_DIR.mkdir(exist_ok=True)

    video_files = [
        f for f in VIDEO_DIR.rglob("*")
        if f.is_file() and f.suffix.lower() in VIDEO_EXTS
    ]

    total = len(video_files)
    if total == 0:
        print("No video files found in videos/")
        return

    created = 0
    skipped = 0
    failed = 0

    print(f"Found {total} video files.")
    print("Generating thumbnails...\n")

    for idx, file in enumerate(video_files, start=1):
        rel_video = file.relative_to(VIDEO_DIR).as_posix()
        thumb_name = get_thumb_name(rel_video)
        thumb_path = THUMB_DIR / thumb_name

        print(f"[{idx}/{total}] {rel_video}")

        if thumb_path.exists():
            skipped += 1
            print("  -> skipped (already exists)\n")
            continue

        ok = make_thumbnail(file, thumb_path)
        if ok:
            created += 1
        else:
            failed += 1

        print()

    print("Done.")
    print(f"Created: {created}")
    print(f"Skipped: {skipped}")
    print(f"Failed:  {failed}")


if __name__ == "__main__":
    main()
