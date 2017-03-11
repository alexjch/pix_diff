import os
from detector import calc_size, INSET_PIXELS
from PIL import Image, ImageDraw


def draw_bbox(image_file, bbox, bbox_color="red"):
    img = Image.open(image_file)
    k, _ = calc_size(img.size)
    draw = ImageDraw.Draw(img)
    x0, y0, x1, y1 = [int(coord) + INSET_PIXELS for coord in bbox]
    draw.rectangle(((x0, y0), (x1, y1)), outline=bbox_color)
    of = os.path.basename(image_file)
    dn = os.path.dirname(image_file)
    fp = os.path.join(dn, '_{}'.format(of))
    img.save(fp)
    return fp
