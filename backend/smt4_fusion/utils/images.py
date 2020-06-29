import cv2
import numpy as np
from PIL import Image, ImageOps, ImageChops

def crop_to_content(img, bg_color):
    bg = Image.new(img.mode, img.size, bg_color)
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()
    if bbox:
        return img.crop(bbox)


def replace_alpha(img, color=(0, 0, 0)):
    bg = Image.new('RGB', img.size, color)
    bg.paste(img, (0, 0), img)
    return bg


def crop_largest_object(img):
    img_arr = np.array(img)
    gray = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
    _, thresh_gray = cv2.threshold(gray, thresh=0, maxval=255, type=cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(thresh_gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    _, (x, y, w, h) = sorted(
        [(contour, cv2.boundingRect(contour)) for contour in contours],
        key=lambda i: i[1][2]*i[1][3],
        reverse=True,
    )[0]

    return Image.fromarray(img_arr[y:y+h, x:x+w])
