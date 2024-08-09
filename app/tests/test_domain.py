import pytest

from app.domain.entities import Meme
from app.domain.exceptions import NotSupportedFileExtensionException
from app.domain.value_objects import MIMETypes


def test_can_create_meme():
    meme = Meme(filename="image.jpg")
    assert meme, "Should be able to create meme."
    assert meme.filename == "image.jpg", "File name do not match."


def test_can_create_meme_without_description():
    meme = Meme(filename="image.jpg")
    assert meme.description is None, "Should be able to create meme without description."


def test_can_create_meme_with_description():
    meme = Meme(filename="image.jpg", description="My image")
    assert meme.description == "My image", "Should be able to create meme with description."


def test_supports_different_formats():
    meme = Meme("image.bmp")
    assert meme, "Should support 'bmp' format"

    meme = Meme("image.gif")
    assert meme, "Should support 'gif' format"

    meme = Meme("image.jpeg")
    assert meme, "Should support 'jpeg' format"

    meme = Meme("image.jpg")
    assert meme, "Should support 'jpg' format"

    meme = Meme("image.png")
    assert meme, "Should support 'png' format"

    meme = Meme("image.webp")
    assert meme, "Should support 'webp' format"

    meme = Meme("image.mp4")
    assert meme, "Should support 'mp4' format"

    meme = Meme("image.mpeg")
    assert meme, "Should support 'mpeg' format"

    meme = Meme("image.webm")
    assert meme, "Should support 'webm' format"


def test_correct_MIME_type():
    meme = Meme("image.jpg")
    assert meme.content_type.name == "jpeg"
    assert meme.content_type.value == "image/jpeg"


def test_exception_on_unsupported_format():
    with pytest.raises(NotSupportedFileExtensionException):
        Meme("file.exe")
        pytest.fail(f"Should not support formats other than {list(MIMETypes.supported_types())}")


def test_exception_on_file_without_format():
    with pytest.raises(NotSupportedFileExtensionException):
        Meme("qwerty")
        pytest.fail(
            "Can't save file without extension. "
            f"Should not support formats other than {list(MIMETypes.supported_types())}."
        )


def test_exception_file_named_as_format():
    with pytest.raises(NotSupportedFileExtensionException):
        Meme("jpg")
        pytest.fail(
            "Can't save file named as extension. File should be named as followed: 'name.extension'"
            f"Should not support formats other than {list(MIMETypes.supported_types())}"
        )
