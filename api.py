import shutil
from typing import List
from fastapi import UploadFile, File, APIRouter, Form
from schemas import UploadVideo, Message
from models import Video, User


video_router = APIRouter()


@video_router.post('/')
async def create_video(
        title: str = Form(...), description: str = Form(...), file: UploadFile = File(...)
):
    # Укакзываем валидатор
    info = UploadVideo(title=title, description=description)
    with open(f'{file.filename}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    user = await User.objects.first()
    return await Video.objects.create(file=file.filename, user=user, **info.dict())


@video_router.get("/video/{video_pk}", response_model=Video, responses={404: {"model": Message}})
async def get_video(video_pk):
    return await Video.objects.select_related('user').get(pk=video_pk)


