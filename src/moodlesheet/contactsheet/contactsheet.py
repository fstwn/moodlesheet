# Based on contactsheet
#
# Original Script Copyright (c) 2018, Paul Butcher
# 
# https://github.com/paul-butcher/contactsheet
# MIT license
#
# Modified by Max Eschenbach, 2022 DDU, TU Darmstadt

# PYTHON STANDARD LIBRARY IMPORTS ---------------------------------------------

import math
from statistics import mean


# THIRD PARTY LIBRARY IMPORTS -------------------------------------------------

from PIL import Image, ImageOps


def create_tiled_image(image_paths, mode="original",
                       factor=0.0, wm=0, hm=0, center=True,
                       background="black"):
    """
    Create a tiled image from the list of image paths.
    """
    image_count = len(image_paths)
    if image_count == 0:
        return Image.new("RGB", (1, 1), "black")
    grid_size = get_grid_size(image_count)
    if mode == "average":
        # takes average image size in collection as tile size
        sizes = [Image.open(img).size for img in image_paths]
        image_size = (int(math.floor(mean([s[0] for s in sizes]))),
                      int(math.floor(mean([s[1] for s in sizes]))))
    elif mode == "floor":
        # takes smallest image size in collection as tile size
        sizes = [Image.open(img).size for img in image_paths]
        image_size = (int(math.floor(min([s[0] for s in sizes]))),
                      int(math.floor(min([s[1] for s in sizes]))))
        # takes first image size in collection as tile size
    else:
        image_size = Image.open(image_paths[0]).size
    tile_size, output_size = get_tiled_image_dimensions(grid_size,
                                                        image_size,
                                                        factor=factor,
                                                        wm=wm,
                                                        hm=hm)
    
    final_image = Image.new("RGB", output_size, background)

    for i, image_path in enumerate(image_paths):
        insert_image_into_grid(final_image,
                               tile_size,
                               image_path,
                               get_location_in_grid(grid_size, i),
                               center=center,
                               wm=wm,
                               hm=hm)

    return final_image


def get_grid_size(cell_count):
    """
    Determines the best grid shape for a given cell count.
    The best grid shape is the one closest to square that minimises the number
    of blank cells.
    e.g. for a square number, it is the corresponding square root.
    >>> get_grid_size(25)
    (5, 5)
    It will otherwise be a rectangle, with the one value matching the
    square root
    >>> get_grid_size(20)
    (5, 4)
    If the number does not fit perfectly into such a rectangle, then it will
    be a rectangle the next size up.
    >>> get_grid_size(15)
    (4, 4)
    """
    sqrt = math.sqrt(cell_count)
    sqrt_floor = int(math.floor(sqrt))
    if sqrt == sqrt_floor:
        # perfect square
        cols = sqrt_floor
        rows = sqrt_floor
    else:
        # Otherwise, this is a rectangle.
        # Expand cols to accommodate
        cols = sqrt_floor + 1
        # Expand rows if needed
        rows = sqrt_floor + (1 if cell_count > sqrt_floor * cols else 0)

    # PIL image sizes are width x height - analogous with cols x rows
    return cols, rows


def get_tiled_image_dimensions(grid_size, image_size, factor=0.0, wm=0, hm=0):
    """
    An image consisting of tiles of itself (or same-sized) images
    will be close to the same dimensions as the original.
    This returns two tuples - the size of the final output image, and the size
    of the tiles that it will consist of.
    :param grid_size: A 2-tuple (width, height) defining the shape of the grid
                      (in number of images)
    :param image_size: A 2-tuple (width, height) defining the shape of the
                       final image (in pixels)
    :return: two 2-tuples, the size of each tile and the size of the final
             output image/
    """
    if not factor:
        tile_width = int(image_size[0] / grid_size[0]) + wm
        # preserve aspect ratio by dividing consistently.
        # grid cols is always >= rows
        tile_height = int(image_size[1] / grid_size[0]) + hm
    else:
        tile_width = int(image_size[0] * factor) + wm
        tile_height = int(image_size[1] * factor) + hm

    # find the final width and height by multiplying up the tile size by the
    # number of rows / cols.
    final_width = (tile_width * grid_size[0]) + (wm * grid_size[0]) + wm
    final_height = (tile_height * grid_size[1]) + (wm * grid_size[1]) + hm

    return (tile_width, tile_height), (final_width, final_height)


def insert_image_into_grid(final_image, tile_size, image_path, location,
                           wm=0, hm=0, center=True):
    """
    Given a PIL image object - `final_image`, insert the image found at
    `image_path` into the appropriate `location` and return it.
    location is defined as the 2d location in a grid of images
    (see get_location_in_grid)
    """
    input_image = Image.open(image_path)
    input_image.thumbnail(tile_size)
    # get width and height from thumbnailed image
    width, height = input_image.size
    # compute addition to with and height to center the
    # inserted image in the tile
    wadd = 0
    hadd = 0
    if center:
        wadd += int(math.floor((tile_size[0] - width) / 2)) 
        hadd += int(math.floor((tile_size[1] - height) / 2))
    # compute x and y location of image insertion
    x = (tile_size[0] * location[0]) + (wm * location[0]) + wm + wadd
    y = (tile_size[1] * location[1]) + (hm * location[1]) + hm + hadd
    # insert image
    final_image.paste(input_image, (x, y))
    # return result
    return final_image


def get_location_in_grid(grid, index):
    """
    Given an index position into a flat list, and a grid (cols, rows). Return
    the col, row position of that index, assuming a horizontal-first view.
    e.g.
    +---+---+---+
    | 0 | 1 | 2 |
    +---+---+---+
    | 3 | 4 | 5 |
    +---+---+---+
    | 7 | 8 | 9 |
    +---+---+---+
    >>> get_location_in_grid((3, 3), 4)
    (1, 1)
    >>> get_location_in_grid((4, 3), 6)
    (2, 1)
    >>> get_location_in_grid((3, 4), 4)
    (1, 1)
    """

    return index % grid[0], int(math.floor(index / grid[0]))