import shutil

from fastapi import APIRouter, UploadFile, BackgroundTasks

from app.services.images import ImagesService
from app.tasks.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Изображение отелей"])


@router.post("")
async def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
    ImagesService().upload_image(file, background_tasks)
