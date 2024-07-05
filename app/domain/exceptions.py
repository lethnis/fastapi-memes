from dataclasses import dataclass

from app.domain.value_objects import MIMETypes


@dataclass(eq=False)
class NotSupportedFileExtensionException(Exception):
    filename: str

    @property
    def message(self):
        return (
            f"Не поддерживаемый формат файла '{self.filename}'."
            f"Поддерживаются следующие типы данных: {MIMETypes.supported_types()}"
        )
