from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .config import VIDEO_DIR, THUMB_DIR, STATIC_DIR, TEMPLATES_DIR
from .services import scan_videos

VIDEO_DIR.mkdir(exist_ok=True)
THUMB_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)
TEMPLATES_DIR.mkdir(exist_ok=True)

app = FastAPI()
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

app.mount("/videos", StaticFiles(directory=str(VIDEO_DIR)), name="videos")
app.mount("/thumbnails", StaticFiles(directory=str(THUMB_DIR)), name="thumbnails")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, q: str = ""):
    videos = scan_videos(q)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"videos": videos, "query": q}
    )

@app.get("/player", response_class=HTMLResponse)
async def player(request: Request, video: str):
    return templates.TemplateResponse(
        request=request,
        name="player.html",
        context={"video_url": video}
    )
