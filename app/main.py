from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .config import VIDEO_DIR, THUMB_DIR, STATIC_DIR, TEMPLATES_DIR
from .services import scan_videos
from pathlib import Path
from urllib.parse import quote
from .services import scan_videos, paginate_items, get_search_keywords

VIDEO_DIR.mkdir(exist_ok=True)
THUMB_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)
TEMPLATES_DIR.mkdir(exist_ok=True)

app = FastAPI()
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

app.mount("/videos", StaticFiles(directory=str(VIDEO_DIR)), name="videos")
app.mount("/thumbnails", StaticFiles(directory=str(THUMB_DIR)), name="thumbnails")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/playlist", response_class=HTMLResponse)
async def playlist(request: Request, q: str = ""):
    videos = scan_videos(q)

    return templates.TemplateResponse(
        request=request,
        name="playlist.html",
        context={
            "videos": videos,
            "query": q,
            "initial_video": videos[0] if videos else None,
        }
    )

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, q: str = "", page: int = 1):
    videos = scan_videos(q)
    keywords = get_search_keywords()
    pagination = paginate_items(videos, page=page, per_page=25)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "videos": pagination["items"],
            "query": q,
            "keywords": keywords,
            "page": pagination["page"],
            "total_pages": pagination["total_pages"],
            "total_items": pagination["total_items"],
            "has_prev": pagination["has_prev"],
            "has_next": pagination["has_next"],
            "prev_page": pagination["prev_page"],
            "next_page": pagination["next_page"],
        }
    )

@app.get("/player", response_class=HTMLResponse)
async def player(request: Request, video: str):
    safe_video_url = quote(video, safe="/")
    
    return templates.TemplateResponse(
        request=request,
        name="player.html",
        context={"video_url": safe_video_url,
                 "video_name": Path(video).name,
        }
    )
