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

@app.get("/video/blackwhite")
async def get_black_white_video(video_url: str):
    response = requests.get(video_url, stream=True)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch video file")

    temp_input_file = "temp_video_input.mp4"
    temp_output_file = "temp_video_output.mp4"

    with open(temp_input_file, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)

    try:
        subprocess.run(["ffmpeg", "-i", temp_input_file, "-vf", "hue=s=0", "-c:a", "copy", temp_output_file], check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        raise HTTPException(status_code=500, detail="Failed to convert video to black and white")

    with open(temp_output_file, "rb") as file:
        output_video = file.read()

    os.remove(temp_input_file)
    os.remove(temp_output_file)

    return output_video
