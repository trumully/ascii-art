from enum import Enum
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
from PIL import Image, ImageEnhance


class AsciiType(Enum):
    """Classifies the character sets used for the ASCII art.

    Attributes:
        SIMPLE (str): A simple character set.
        BARS (str): A character set with varying shades.
        COMPLEX (str): A complex character set.
    """

    SIMPLE = "@%#*+=-:. "
    BARS = "█▓▒░ "
    COMPLEX = (
        '$@B%8&WM#*zcvunxrjft/\\|()1{}[]?-_+~<>i!lI;;::,,,"""^^^'
        "`````'''''.......     "
    )


def get_sizes(image: np.ndarray, num_columns: int) -> tuple[int, ...]:
    """Get the sizes of the image and the cells.

    Args:
        image (np.ndarray): The image to be converted to ASCII art.
        num_columns (int): The number of columns in the ASCII art.

    Returns:
        tuple[int, ...]: The width, height, cell_width, cell_height, and
                        num_rows of the image.
    """
    height, width = image.shape
    cell_width = width / num_columns
    cell_height = 2 * cell_width
    num_rows = round(height / cell_height)
    return width, height, cell_width, cell_height, num_rows


def enhance_image(
    path: Path, brightness: Optional[int] = None, contrast: Optional[int] = None
) -> Image:
    """With a given image, enhance the brightness and contrast if provided.

    Args:
        path (Path): The path to the image
        brightness (Optional[int], optional): The brightness value. Defaults to None.
        contrast (Optional[int], optional): The contrast value. Defaults to None.

    Returns:
        Image: The enhanced image.
    """
    image = Image.open(path)

    if contrast is not None:
        image = ImageEnhance.Contrast(image).enhance(contrast)
    if brightness is not None:
        image = ImageEnhance.Brightness(image).enhance(brightness)

    return image


def colorize_text(text: str, r: int, g: int, b: int) -> str:
    """Colorize the text with the given RGB values.

    Args:
        text (str): The text to be colorized.
        r (int): The red value.
        g (int): The green value.
        b (int): The blue value.

    Returns:
        str: _description_
    """
    return f"\u001b[38;2;{r};{g};{b}m{text}\u001b[0m"


def grayscale_image(image: Image) -> np.array:
    """Convert an image to grayscale.

    Args:
        image (Image): The image to be converted to grayscale.

    Returns:
        np.array: The grayscale image.
    """
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)


def image_to_ascii(
    path: Path,
    num_columns: int = 100,
    ascii_mode: AsciiType = AsciiType.COMPLEX,
    brightness: Optional[int] = None,
    contrast: Optional[int] = None,
) -> str:
    """Convert an image to ASCII art.

    Args:
        path (Path): The path to the image.
        num_columns (int, optional): The number of columns. Defaults to 100.
        ascii_mode (AsciiType, optional): The character set to use.
                                          Defaults to AsciiType.COMPLEX.
        brightness (Optional[int], optional): Brightness value. Defaults to None.
        contrast (Optional[int], optional): Amount of contrast. Defaults to None.

    Returns:
        str: The ascii art.
    """
    num_chars = len(ascii_mode.value)

    image: np.ndarray = grayscale_image(enhance_image(path, brightness, contrast))

    width, height, cell_width, cell_height, num_rows = get_sizes(image, num_columns)

    output_str = ""
    for i in range(num_rows):
        for j in range(num_columns):
            output_str += ascii_mode.value[
                min(
                    int(
                        np.mean(
                            image[
                                int(i * cell_height) : min(
                                    int((i + 1) * cell_height), height
                                ),
                                int(j * cell_width) : min(
                                    int((j + 1) * cell_width), width
                                ),
                            ]
                        )
                        * num_chars
                        / 255
                    ),
                    num_chars - 1,
                )
            ]
        output_str += "\n"
    return output_str
