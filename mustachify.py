from PIL import Image, ImageDraw, ImageOps
from face_recognition import face_landmarks, face_locations
import numpy as np


def load_image_file(file, mode='RGB'):
    """
    Loads an image file (.jpg, .png, etc) into a numpy array
    :param file: image file name or file object to load
    :param mode: format to convert the image to. Only 'RGB' (8-bit RGB, 3 channels) and 'L' (black and white) are supported.
    :return: image contents as numpy array
    """
    im = Image.open(file)
    # handle rotations (https://izziswift.com/pil-thumbnail-is-rotating-my-image/)
    # https://pillow.readthedocs.io/en/latest/reference/ImageOps.html#PIL.ImageOps.exif_transpose
    im = ImageOps.exif_transpose(im)
    im = im.convert(mode)
    return np.array(im)
    

def mustachify(file, mustache_file="mustache.png"):
    """
    Pastes a mustache on each face in the image file

    :param file: image file name or file object to load
    :param mustache_file: file pointer to mustache png
    :return: PIL image object with mustache on each face
    """
    # load file to img
    img_array = load_image_file(file)
    # get landmarks of all faces
    locations = face_locations(img_array, number_of_times_to_upsample=1)
    landmarks = face_landmarks(img_array, face_locations=None)
    # create PIL object for img and drawing
    img = Image.fromarray(img_array)
    draw = ImageDraw.Draw(img)
    # load mustache
    mustache = Image.open(mustache_file)
    # loop over each face
    for face in landmarks:
        # scale mustache to size of top lip
        xmouth = list(zip(*face["top_lip"]))[0]
        mouthwidth = max(xmouth) - min(xmouth)
        x, y = mustache.size
        ratio = mouthwidth / x * 2
        mask = mustache.resize((int(x*ratio)+1, int(y*ratio)+1))
        pos = face["nose_tip"][0][0]-int(mouthwidth/1.4), face["nose_tip"][0][1] - int(mouthwidth/4)
        img.paste(mask, pos, mask)
    return img  