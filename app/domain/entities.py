from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from app.domain.exceptions import NotSupportedFileExtensionException
from app.domain.value_objects import MIMETypes


@dataclass
class Meme:

    id: str = field(init=False, default_factory=lambda: str(uuid4()))
    filename: str
    description: str | None = field(default=None)
    content_type: type[MIMETypes] = field(init=False)
    created_at: datetime | None = field(init=False, default=None)
    updated_at: datetime | None = field(init=False, default=None)

    def __post_init__(self):
        name_and_extension = self.filename.lower().split(".")
        if len(name_and_extension) < 2 or name_and_extension[-1] not in MIMETypes.supported_types():
            raise NotSupportedFileExtensionException(self.filename)
        self.content_type = MIMETypes[name_and_extension[-1]]
