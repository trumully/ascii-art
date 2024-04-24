import pytest
from pathlib import Path
from ascii_art.image_to_ascii import image_to_ascii, AsciiType


def test_image_to_ascii_basic():
    path = Path("assets/truman_1.png")
    ascii_art = image_to_ascii(path)
    assert isinstance(ascii_art, str)


def test_image_to_ascii_num_columns():
    path = Path("assets/truman_1.png")
    ascii_art = image_to_ascii(path, num_columns=50)
    assert isinstance(ascii_art, str)


def test_image_to_ascii_ascii_mode():
    path = Path("assets/truman_1.png")
    ascii_art = image_to_ascii(path, ascii_mode=AsciiType.SIMPLE)
    assert isinstance(ascii_art, str)


def test_image_to_ascii_brightness():
    path = Path("assets/truman_1.png")
    ascii_art = image_to_ascii(path, brightness=10)
    assert isinstance(ascii_art, str)


def test_image_to_ascii_contrast():
    path = Path("assets/truman_1.png")
    ascii_art = image_to_ascii(path, contrast=10)
    assert isinstance(ascii_art, str)


def test_image_to_ascii_primary_color():
    path = Path("assets/truman_1.png")
    ascii_art = image_to_ascii(path, primary_color=(255, 0, 0))
    assert isinstance(ascii_art, str)


def test_image_to_ascii_background_color():
    path = Path("assets/truman_1.png")
    ascii_art = image_to_ascii(path, background_color=(0, 255, 0))
    assert isinstance(ascii_art, str)


def test_image_to_ascii_invalid_path():
    path = Path("path/to/nonexistent/image.jpg")
    with pytest.raises(FileNotFoundError):
        image_to_ascii(path)
