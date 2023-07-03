from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from extract import *
import os


SECRET = os.getenv("SECRET")

#
app = FastAPI()

class Msg(BaseModel):
    msg: str
    secret: str

@app.get("/")

async def root():
    return {"message": "Hello!"}


@app.get("/homepage")
async def demo_get():
    driver=createDriver()

    homepage = getGoogleHomepage(driver)
    driver.close()
    return homepage

@app.post("/backgroundDemo")
async def demo_post(inp: Msg, background_tasks: BackgroundTasks):
    
    background_tasks.add_task(doBackgroundTask, inp)
    return {"message": "Success, background task started"}
    
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from extract import *
import os
import requests
import subprocess

SECRET = os.getenv("SECRET")

app = FastAPI()

class Msg(BaseModel):
    msg: str
    secret: str

@app.get("/")
async def root():
    return {"message": "Hello!"}

@app.get("/homepage")
async def demo_get():
    driver = createDriver()
    homepage = getGoogleHomepage(driver)
    driver.close()
    return homepage

@app.post("/backgroundDemo")
async def demo_post(inp: Msg, background_tasks: BackgroundTasks):
    background_tasks.add_task(doBackgroundTask, inp)
    return {"message": "Success, background task started"}

@app.get("/video/length")
async def get_video_length(video_url: str):
    response = requests.get(video_url, stream=True)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch video file")

    temp_file = "temp_video.mp4"

    with open(temp_file, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)

    try:
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", temp_file], capture_output=True, text=True)
        video_length = float(result.stdout)
    except (FileNotFoundError, subprocess.CalledProcessError):
        raise HTTPException(status_code=500, detail="Failed to get video length")

    os.remove(temp_file)

    return {"video_length": video_length}


