from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class ImageSchema(BaseModel):
    uuid: UUID
    file: str
    extension_type: str
    width: int
    height: int
    upload_date: datetime | None = None
    finished_date: datetime | None = None
    last_upload_date: datetime | None = None
