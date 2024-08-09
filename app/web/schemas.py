from datetime import datetime
from pydantic import BaseModel, computed_field

from app.config import settings


class MemesResponse(BaseModel):

    id: int
    description: str | None
    filename: str
    content_type: str
    created_at: datetime
    updated_at: datetime

    @computed_field
    def url(self) -> str:
        return f"{settings.ENDPOINT_URL}/{settings.BUCKET_NAME}/{self.filename}"
