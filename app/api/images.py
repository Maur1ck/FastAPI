import shutil

from fastapi import APIRouter, UploadFile, BackgroundTasks

from app.tasks.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Изображение отелей"])

@router.post("")
async def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
    image_path = f"app/static/images/{file.filename}"
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    # resize_image.delay(image_path)
    background_tasks.add_task(resize_image, image_path)