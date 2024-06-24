import aiofiles
from fastapi import APIRouter, UploadFile

from app.tasks.tasks import process_image

router = APIRouter(prefix="/images", tags=["Image download"])


@router.post("/hotels")
async def add_hotel_image(name: int, file_to_upload: UploadFile):
    image_path = f"app/static/images/{name}.webp"
    async with aiofiles.open(image_path, "wb+") as file_object:
        file = await file_to_upload.read()
        await file_object.write(file)
    process_image.delay(image_path)
