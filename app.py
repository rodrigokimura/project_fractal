import numpy as np
from PIL import Image
from PIL.ImageColor import getrgb
from scipy.interpolate import interp1d

from mandelbrot import MandelbrotSet
from viewport import Viewport


def paint(mandelbrot_set: MandelbrotSet, viewport: Viewport, palette, smooth: bool):
    for pixel in viewport:
        stability = mandelbrot_set.stability(complex(pixel), smooth)
        index = int(min(stability * len(palette), len(palette) - 1))
        pixel.color = palette[index % len(palette)]


def denormalize(palette):
    return [tuple(int(channel * 255) for channel in color) for color in palette]


def make_gradient(colors, interpolation="linear"):
    X = [i / (len(colors) - 1) for i in range(len(colors))]
    Y = [[color[i] for color in colors] for i in range(3)]
    channels = [interp1d(X, y, kind=interpolation) for y in Y]
    return lambda x: [np.clip(channel(x), 0, 1) for channel in channels]


def hsb(hue_degrees: int, saturation: float, brightness: float):
    return getrgb(
        f"hsv({hue_degrees % 360}," f"{saturation * 100}%," f"{brightness * 100}%)"
    )


def generate_image_file(width: float):
    SIZE = (1920, 1080)
    MAX_ITERATIONS = 512
    CENTER = -0.7435 + 0.1314j
    WIDTH = 0.01

    args = (SIZE, MAX_ITERATIONS, CENTER, width)

    black = (0, 0, 0)
    blue = (0, 0, 1)
    maroon = (0.5, 0, 0)
    navy = (0, 0, 0.5)
    red = (0.5, 0.5, 0.5)

    colors = [black, navy, blue, maroon, red, black]
    gradient = make_gradient(colors, interpolation="cubic")

    num_colors = 256
    palette = denormalize([gradient(i / num_colors) for i in range(num_colors)])

    mandelbrot_set = MandelbrotSet(max_iterations=MAX_ITERATIONS, escape_radius=1000)

    image = Image.new(mode="RGB", size=SIZE)

    viewport = Viewport(image, center=CENTER, width=width)

    total_pixels = image.height * image.height
    for i, pixel in enumerate(viewport):
        print(f"  Progress: {i / total_pixels:.2%}", end="\r")
        stability = mandelbrot_set.stability(complex(pixel), smooth=True)
        index = int(min(stability * len(palette), len(palette) - 1))
        pixel.color = palette[index % len(palette)]

    image.save(f"{width}.png")
    pass


if __name__ == "__main__":
    for i, w in enumerate([0.003, 0.002, 0.01, 0.05, 0.1, 0.5, 1, 2, 3, 4, 5]):
        print(f"Generating image {i + 1} of 11")
        generate_image_file(w)
