from dataclasses import dataclass, field

from app.domain.exceptions import NotSupportedFileExtensionException
from app.domain.value_objects import MIMETypes


@dataclass
class Meme:

    filename: str
    description: str | None = field(default=None)
    content_type: type[MIMETypes] = field(init=False)

    def __post_init__(self):
        name_and_extension = self.filename.lower().split(".")
        if len(name_and_extension) < 2 or name_and_extension[-1] not in MIMETypes.supported_types():
            raise NotSupportedFileExtensionException(self.filename)
        self.content_type = MIMETypes[name_and_extension[-1]]
