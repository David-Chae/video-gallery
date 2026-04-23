from pathlib import Path
import subprocess
import hashlib
from .config import VIDEO_DIR, THUMB_DIR, VIDEO_EXTS
import math



def get_thumb_name(rel_video: str) -> str:
    return hashlib.md5(rel_video.encode("utf-8")).hexdigest() + ".jpg"

def get_search_keywords() -> list[str]:
    keywords = []

    if not VIDEO_DIR.exists():
        return keywords

    for entry in VIDEO_DIR.iterdir():
        if entry.is_dir():
            keywords.append(entry.name)

    return sorted(keywords, key=str.lower)

def make_thumbnail(video_path: Path, thumb_path: Path):
    if thumb_path.exists():
        return

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
            timeout=20
        )
        if result.returncode != 0:
            print(f"FFMPEG ERROR: {video_path.name}")
            print(result.stderr)
            return False
        
        return thumb_path.exists()
    
    except Exception as e:
        print("Thumbnail error:", e)
        return False

def scan_videos(query: str = ""):
    items = []
    query_terms = query.strip().lower().split()

    for file in VIDEO_DIR.rglob("*"):
        if file.is_file() and file.suffix.lower() in VIDEO_EXTS:
            rel_video = file.relative_to(VIDEO_DIR).as_posix()
            folder = str(file.parent.relative_to(VIDEO_DIR))

            search_text = " ".join([
                file.stem.lower(),      # 파일명: ep1
                file.name.lower(),      # 파일명+확장자: ep1.mkv
                folder.lower(),         # 폴더명: anime
                rel_video.lower(),      # 전체 경로: anime/ep1.mkv
            ])

            if query and query.lower() not in search_text:
                continue

            rel_video = file.relative_to(VIDEO_DIR).as_posix()
            thumb_name = get_thumb_name(rel_video)
            thumb_path = THUMB_DIR / thumb_name

            # 썸네일이 없으면 일단 생성하지 않고 placeholder만 보여줌
            #if not thumb_path.exists():
            #    make_thumbnail(file, thumb_path)

            items.append({
                "name": file.name,
                "stem": file.stem,
                "path": rel_video,  # 추가
                "folder": str(file.parent.relative_to(VIDEO_DIR)),  # 추가
                "video_url": f"/videos/{rel_video}",
                "thumb_url": f"/thumbnails/{thumb_name}" if thumb_path.exists() else "",
            })

    items.sort(key=lambda x: x["name"].lower())
    return items

def paginate_items(items, page: int = 1, per_page: int = 25):
    total_items = len(items)
    total_pages = max(1, math.ceil(total_items / per_page))

    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages

    start = (page - 1) * per_page
    end = start + per_page
    paged_items = items[start:end]

    return {
        "items": paged_items,
        "page": page,
        "per_page": per_page,
        "total_items": total_items,
        "total_pages": total_pages,
        "has_prev": page > 1,
        "has_next": page < total_pages,
        "prev_page": page - 1,
        "next_page": page + 1,
    }
