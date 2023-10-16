import cv2
import numpy as np

from PIL import ImageDraw, Image
from viso_sdk.constants import KEY

from viso_sdk.visualize.palette import get_rgba_color_with_palette_id, get_rgba_color
from viso_sdk.visualize import utils


class VizObjectDraw:
    def __init__(self, bbox_color, bbox_thickness, text_size):
        self.bbox_color = get_rgba_color(bbox_color)
        self.bbox_thickness = bbox_thickness

        self.default_font = utils.init_font(font_size=text_size)

    def _draw_objs_(
            self,
            draw,  # ImageDraw.Draw,
            objs,  # list
            show_label=True,
            show_confidence=True,
            show_class_id=False
    ):
        img_w, img_h = draw.im.size[:2]
        for obj in objs:
            tlwh = obj[KEY.TLWH]

            if tlwh[2] < 1.0:
                x, y, w, h = (np.array(tlwh) * np.array([img_w, img_h, img_w, img_h])).astype(int).tolist()
                # is_relative_coord = True
            else:
                x, y, w, h = np.array(tlwh).astype(int).tolist()
                # is_relative_coord = False

            bbox_color = self.bbox_color if self.bbox_color is not None else get_rgba_color_with_palette_id(
                palette_id=obj.get(KEY.CLASS_ID, 0))

            # put object boundary bbox
            draw.rectangle(xy=[(x, y), (x + w, y + h)], fill=None, outline=bbox_color, width=self.bbox_thickness)

            if show_label:
                label = ""

                if show_class_id and KEY.CLASS_ID in obj.keys():
                    label += f"{obj.get(KEY.CLASS_ID, '')} "

                label += f"{obj.get(KEY.LABEL, '')}"

                if show_confidence:
                    label += f" {float(obj.get(KEY.SCORE)):.2f}"

                # get text label
                if show_label:
                    utils.put_text(
                        font=self.default_font,
                        draw=draw,
                        bbox=(x, y),
                        text=label,
                        bbox_thickness=-1,
                        bbox_color=bbox_color,
                        # show_shadow=True
                    )

        return draw

    def draw_detections(self, img, detections, show_label=True, show_confidence=True):
        # Convert the image to RGB (OpenCV uses BGR)
        cv_im_rgba = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2RGBA)

        # Pass the image to PIL
        pil_base_im = Image.fromarray(cv_im_rgba, "RGBA")

        pil_viz_im = Image.new("RGBA", pil_base_im.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(pil_viz_im, "RGBA")

        self._draw_objs_(
            draw=draw,
            objs=detections,
            show_label=show_label,
            show_confidence=show_confidence)

        pil_out = Image.alpha_composite(pil_base_im, pil_viz_im)
        cv_im_processed = cv2.cvtColor(np.array(pil_out), cv2.COLOR_RGBA2BGR)
        return cv_im_processed

    def draw_tracking(
            self,
            draw,
            tracking
    ):
        pass
