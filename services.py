import shutil
import ormar
from pathlib import Path
from typing import IO, Generator
from uuid import uuid4

import aiofiles
from fastapi import UploadFile, BackgroundTasks, HTTPException
from starlette.requests import Request

from models import Video, User
from schemas import UploadVideo


async def save_video(
        user: User,
        file: UploadFile,
        title: str,
        description: str,
        back_tasks: BackgroundTasks
):
    file_name = f'media/{user.id}_{uuid4()}.mp4'
    if file.content_type == 'video/mp4':
        # back_tasks.add_task(write_video, file_name, file)
        await write_video(file_name, file)
    else:
        raise HTTPException(status_code=418, detail="It isn't mp4")
    info = UploadVideo(title=title, description=description)
    return await Video.objects.create(file=file_name, user=user, **info.dict())


async def write_video(file_name: str, file: UploadFile):
    # Асинхроннно скачиваем файл
    async with aiofiles.open(file_name, "wb") as buffer:
        data = await file.read()
        await buffer.write(data)
    # with open(file_name, "wb") as buffer:
    #     shutil.copyfileobj(file.file, buffer)


def ranged(
        file: IO[bytes],
        start: int = 0,
        end: int = None,
        block_size: int = 8192,
) -> Generator[bytes, None, None]:
    consumed = 0

    file.seek(start)
    while True:
        data_length = min(block_size, end - start - consumed) if end else block_size
        if data_length <= 0:
            break
        data = file.read(data_length)
        if not data:
            break
        consumed += data_length
        yield data

    if hasattr(file, 'close'):
        file.close()


async def open_file(request: Request, video_pk: int) -> tuple:
    """
    Позволяет запускать ролик
    :param request:  Нужен для того чтобы узанть Range
    :param video_pk: Получаем id'шник ролика
    """
    try:
        # Получаем видео
        file = await Video.objects.get(pk=video_pk)
    except ormar.exceptions.NoMatch:
        # Если видео нет просто рейзим 404
        raise HTTPException(status_code=404, detail="Not found")
    # Находим файл
    path = Path(file.dict().get('file'))
    # Открываем его
    file = path.open('rb')
    # Узнаем его размер
    file_size = path.stat().st_size

    content_length = file_size
    status_code = 200
    headers = {}  # Пустой  словарь для заголовков
    content_range = request.headers.get('range')  # Достаем range из заголовка, чтобы знать какой range передается

    if content_range is not None:
        content_range = content_range.strip().lower()
        content_ranges = content_range.split('=')[-1]
        range_start, range_end, *_ = map(str.strip, (content_ranges + '-').split('-'))
        range_start = max(0, int(range_start)) if range_start else 0
        range_end = min(file_size - 1, int(range_end)) if range_end else file_size - 1
        content_length = (range_end - range_start) + 1
        # Указываем начало файла и конец и отдаем файл с опр места
        file = ranged(file, start=range_start, end=range_end + 1)
        status_code = 206
        # Передаем байты ролика для стриминга -> Что позволит нам узнать с какого места мы отдаем файл и прислать
        # следующие данные
        headers['Content-Range'] = f'bytes {range_start}-{range_end}/{file_size}'

    return file, status_code, content_length, headers
