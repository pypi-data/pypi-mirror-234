import os
import PIL
from PIL import ImageFont

from viso_sdk.constants import FONTS_DIR
from viso_sdk.logging import get_logger

pil_version = PIL.__version__
logger = get_logger("vis-font")


DEFAULT_FONT_SIZE = 15
DEFAULT_FONT_NAME = "Roboto-Medium"
DEFAULT_TXT_COLOR = (255, 255, 255, 1.0)
# DEFAULT_TXT_THICKNESS = 1
DEFAULT_SHADOW_COLOR = (0, 0, 0, 1.0)
DEFAULT_OPACITY = 100


DEFAULT_ROI_COLOR = (255, 150, 113, 0.4)
DEFAULT_ROI_OUTLINE_COLOR = (70, 70, 70, 1.0)
DEFAULT_ROI_OUTLINE_THICKNESS = 1
DEFAULT_LABEL_COLOR = (255, 255, 255, 0.4)
DEFAULT_LABEL_SIZE = 50


def get_adjust_bbox_thick(img_sz):
    img_h, img_w = img_sz
    bbox_thick = int(0.5 * (img_h + img_w) / 1000)
    if bbox_thick < 2:
        bbox_thick = 2

    return bbox_thick


def get_text_size(draw, text, font, xy=(10, 10)):
    # calculate area to put text
    if pil_version < "10.0.0":
        text_width, text_height = draw.textsize(text, font)
    else:
        # Get the bounding box of the text
        bbox = draw.textbbox(xy, text, font=font)

        # Calculate the dimensions of the bounding box
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    return text_width, text_height


def get_supported_fonts(fonts_dir=FONTS_DIR):
    font_names = [os.path.splitext(fn)[0] for fn in os.listdir(fonts_dir) if os.path.splitext(fn)[1] == '.ttf']
    return font_names


def get_adjusted_font(bbox_size):
    box_width, box_height = bbox_size

    font_size = max(int(box_height * 0.8), 10)
    font = init_font(font_size=font_size)

    return font


def init_font(font_name=None, font_size=DEFAULT_FONT_SIZE):
    fonts = get_supported_fonts(FONTS_DIR)
    if font_name is not None and os.path.isabs(font_name) and os.path.exists(font_name):
        font_file = font_name
    elif font_name in fonts:
        # logger.warning(f"can not fine such font file {font_name}, use default {fonts[0]}")
        font_file = os.path.join(FONTS_DIR, f"{font_name}.ttf")
    else:
        # logger.warning(f"font_name is not specified, use default {fonts[0]}")
        font_file = os.path.join(FONTS_DIR, f"{fonts[0]}.ttf")
        # font_file = os.path.join(FONTS_DIR, f"SIMSUN.ttf")

    # logger.info(f"load font {font_name}")
    font = ImageFont.truetype(font_file, font_size)
    return font


def put_text(
        draw,
        font,
        bbox,  # tlwh
        text,
        text_color=DEFAULT_TXT_COLOR,
        large_padding=False,
        bbox_thickness=-1,
        bbox_color=None,
        show_shadow=False,
        shadow_color=DEFAULT_SHADOW_COLOR
):
    text_width, text_height = get_text_size(draw=draw, text=text, font=font, xy=bbox[:2])

    padding = max(int(text_height // 4), 2)
    padding_left = padding
    if large_padding:
        padding_top = padding * 2
    else:
        padding_top = padding // 2

    if len(bbox) == 4:  # bbox
        x, y, w, h = bbox[:4]
    else:
        x, y = bbox[:2]
        w, h = text_width, text_height

    x1 = x
    y1 = y
    x2 = x + w
    y2 = y + h

    # Calculate the center coordinates of the bbox
    x_cen = x + w // 2
    y_cen = y + h // 2

    # Calculate the position to center the text
    x_text = x1 + padding_left  # x_cen - text_width / 2
    y_text = y_cen - text_height // 2 - padding_top

    if bbox_color is not None:
        if bbox_thickness == -1:
            # put filled text rectangle
            draw.rectangle(xy=[(x1, y1), (x2, y2)], fill=bbox_color)
        else:
            draw.rectangle(xy=[(x1, y1), (x2, y2)], outline=bbox_color, width=bbox_thickness)
    else:
        pass

    # shadow effect
    if show_shadow:
        draw.multiline_text(
            (x_text + 1, y_text + 1),
            font=font, text=text, fill=shadow_color)

    # put text above rectangle
    draw.multiline_text(
        (x_text, y_text),
        font=font, text=text, fill=text_color)

    return draw
