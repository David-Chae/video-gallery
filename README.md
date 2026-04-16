# Video Gallery
A local FastAPI-based video gallery that scans folders, generates thumbnails, supports filename search, and plays videos in the browser.
로컬 폴더의 비디오 파일을 갤러리 형태로 보여주고, 썸네일과 검색 기능을 제공하는 FastAPI 기반 웹 앱입니다.

## Features
- 비디오 파일 자동 탐색 : automatic scanning of videos.
- 썸네일 표시 : display thumbnails.
- 파일명 검색 : search file names.
- 브라우저에서 비디오 재생 : play videos from browser.

## Project Structure
- `app/`: 애플리케이션 코드 application code.
- `videos/`: 원본 비디오 저장 폴더 original video storage folder.
- `thumbnails/`: 썸네일 저장 폴더 thumbnail image storage folder.

## Setup
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create videos and thumbnails folder in video-gallery folder which already contain app folder.
app 폴더가 있는 video-gallery 폴더 안에 videos 그리고 thumbnails 폴더를 만들것.

Put your video files in the videos folder.
비디오 파일을 videos 폴더 안에 넣을것.

## How to Run
```bash
uvicorn app.main:app --reload
```
Access http://127.0.0.1:8000 from browser.
