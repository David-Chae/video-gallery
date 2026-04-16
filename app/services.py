from pathlib import Path
import subprocess
from .config import VIDEO_DIR, THUMB_DIR, VIDEO_EXTS

def make_thumbnail(video_path: Path, thumb_path: Path):
    if thumb_path.exists():
        return

    cmd = [
        "ffmpeg",
        "-y",
        "-ss", "00:00:03",
        "-i", str(video_path),
        "-frames:v", "1",
        str(thumb_path)
    ]
    try:
        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=20
        )
    except Exception:
        pass

def scan_videos(query: str = ""):
    items = []

    for file in VIDEO_DIR.rglob("*"):
        if file.is_file() and file.suffix.lower() in VIDEO_EXTS:
            if query and query.lower() not in file.stem.lower():
                continue

            rel_video = file.relative_to(VIDEO_DIR).as_posix()
            thumb_name = rel_video.replace("/", "__") + ".jpg"
            thumb_path = THUMB_DIR / thumb_name

            if not thumb_path.exists():
                make_thumbnail(file, thumb_path)

            items.append({
                "name": file.name,
                "stem": file.stem,
                "video_url": f"/videos/{rel_video}",
                "thumb_url": f"/thumbnails/{thumb_name}" if thumb_path.exists() else "",
            })

    items.sort(key=lambda x: x["name"].lower())
    return items
