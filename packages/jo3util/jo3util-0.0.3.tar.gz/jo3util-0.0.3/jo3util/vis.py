#! /usr/bin/env python3
# vim:fenc=utf-8
import jax
import numpy as np
from PIL import Image

def to_rgb(x):
    x = x / x.max() * 255
    x = np.broadcast_to(x, (3, x.shape[1], x.shape[2]))
    return x.astype("uint8")


def to_img(x, scale_up=10):
    x = to_rgb(x)

    img = np.empty(
        (x.shape[1] * scale_up, x.shape[2] * scale_up, x.shape[0]), dtype=np.uint8
    )

    for color in range(x.shape[0]):
        for row in range(x.shape[1]):
            for col in range(x.shape[2]):
                pixel = x[color, row, col]
                new_row = row * scale_up
                new_col = col * scale_up
                img[
                    new_row : new_row + scale_up,
                    new_col : new_col + scale_up,
                    color,
                ] = pixel
    if x.shape[0] == 1:
        return Image.fromarray(img.squeeze())
    else:
        return Image.fromarray(img, "RGB")


def color_mask(x, mask, color=np.array([255, 0, 0])):
    if len(mask.shape) == 2:
        mask = np.broadcast_to(mask, (3, mask.shape[0], mask.shape[1]))

    x = to_rgb(x)
    x = x * (1 - mask)
    color = jax.vmap(lambda x, y: x * y, (0, 0))(color, mask)
    x = x + color

    return x
