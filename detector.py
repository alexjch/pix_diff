import os
from PIL import Image, ImageChops, ImageFilter, ImageOps

MIN_AREA = 250      # Threshold pixels to consider a change in an image acceptable
IMG_W = 750         # Width to resize image
INSET_PIXELS = 5    # Number of pixels to crop from image border
MIN_LEVEL = 70      #


def calc_size(size, w=IMG_W):
    k = w / size[0]
    return k, (w, int(k * size[1]))


def prep_frame(frame, size):
    blur = ImageFilter.GaussianBlur(radius=5)
    return frame\
        .resize(size)\
        .convert('L')\
        .filter(blur)


def change(file_a, file_b):
    threshold = MIN_LEVEL
    image_a = Image.open(file_a)
    k, size = calc_size(image_a.size)
    image_a = prep_frame(image_a, size)
    image_b = prep_frame(Image.open(file_b), size)
    image_diff = ImageChops.difference(image_a, image_b)
    image_diff = image_diff.point(lambda p: p > threshold and 255)\
                           .filter(ImageFilter.CONTOUR)
    image_diff = ImageOps.crop(image_diff, border=INSET_PIXELS)
    bounding_box = ImageOps.invert(image_diff).getbbox()
    if bounding_box is not None:
        return [int((z+5)/k) for z in bounding_box]


def min_area(bounding_box):
    x0, y0, x1, y1 = bounding_box
    area = (x1 - x0) * (y1 - y0)
    return area > MIN_AREA


class VideoMonitor:

    def __init__(self, background=None):
        self.background = background

    def has_change(self, next_frame):
        if self.background is not None:
            print('comparing {} to {}'.format(os.path.basename(self.background), os.path.basename(next_frame)))
            bounding_box = change(self.background, next_frame)
            if bounding_box is None or min_area(bounding_box) is False:
                print('No change found between {} and {}'.format(self.background, next_frame))
                return False, None
            return True, bounding_box
        return None, None
