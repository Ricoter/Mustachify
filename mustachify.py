from PIL import Image, ImageDraw, ImageOps
from face_recognition import face_landmarks, face_locations
import numpy as np


def load_image_file(file, mode="RGB"):
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


def angle(a,b):
    """
    Finds angle in degrees of the line between point a and point b
    """
    x = b[0]-a[0]
    y = b[1]-a[1]
    print(y)
    return np.arctan(y/x)


def face_angle(landmark):
    """
    Finds the angle of the face based on the outer corners of the eye-landmarks

    :return: angel of face in degrees
    """
    if len(landmark) == 3:  # model="small"
        lEyeOut = landmark["left_eye"][0]
        rEyeOut = landmark["right_eye"][0]
    elif len(landmark) == 9: # model="large"
        lEyeOut = landmark["left_eye"][0]
        rEyeOut = landmark["right_eye"][3]
    else:
        raise ValueError("Landmarks model should be \"small\" or \"large\"")
    return angle(a=lEyeOut, b=rEyeOut)


def rotate(img, landmark, ref=None):
    """[summary] # TODO DocString

    Args:
        img ([type]): [description]
        landmark ([type]): [description]
        ref ([type], optional): [description]. Defaults to None.

    Returns:
        [type]: [description]
    """
    alpha = -face_angle(landmark)
    alpha = np.rad2deg(alpha)
    print(alpha)
    if ref == None:
        return img.rotate(alpha, resample=Image.BICUBIC, expand=True) # degrees counter-clockwise
    else:
        return (
            img.rotate(alpha, resample=Image.BICUBIC, expand=True), 
            ref.rotate(alpha, resample=Image.BICUBIC, expand=True),
        )


def scale(img, landmark, ref=None, scale=2):
    """[summary] # TODO DocString

    Args:
        img ([type]): [description]
        landmark ([type]): [description]
        ref ([type], optional): [description]. Defaults to None.
        scale (int, optional): [description]. Defaults to 2.

    Raises:
        ValueError: [description]

    Returns:
        [type]: [description]
    """
    if len(landmark) == 3:  # model="small"
        lEyeOut = landmark["left_eye"][0]
        rEyeOut = landmark["right_eye"][0]
    elif len(landmark) == 9: # model="large"
        lEyeOut = landmark["left_eye"][0]
        rEyeOut = landmark["right_eye"][3]
    else:
        raise ValueError("Landmarks model should be \"small\" or \"large\"")
    span = ((lEyeOut[0]-rEyeOut[0])**2 + (lEyeOut[1]-lEyeOut[1])**2)**.5
    ratio = span / img.size[0] * scale
    new_size = round(img.size[0]*ratio), round(img.size[1]*ratio)
    if ref==None:
        return img.resize(new_size)
    else:
        return img.resize(new_size), ref.resize(new_size)


def removePadding(img, ref=None):
    """
    Removes transparent padding of img (and reference img)

    :param img: PIL image object to remove padding from
    :param ref: PIL image object that is used for a reference point
    :return: 
    """
    if ref == None:
        return img.crop(img.getbbox())
    else:
        box = img.getbbox()
        return img.crop(box), ref.crop(box)


def mustachify(
    file, 
    mustache_file="mustache.png", 
    rotation=True,
    perspective=False, # TODO add perspective transformation
    modelsize="small",
    ):
    """
    Pastes a mustache on each face in the image file

    :param file: image file name or file object to load
    :param mustache_file: file pointer to mustache png
    :return: PIL image object with mustache on each face
    """
    if modelsize not in ("small", "large"):
        raise ValueError("Landmarks model should be \"small\" or \"large\"")

    # load file to img
    img_array = load_image_file(file)
    # get landmarks of all faces
    locations = face_locations(img_array, number_of_times_to_upsample=1)
    landmarks = face_landmarks(img_array, face_locations=None, model=modelsize)
    # create PIL object for img and drawing
    img = Image.fromarray(img_array)
    draw = ImageDraw.Draw(img)
    # load mustache
    mustache = Image.open(mustache_file)
    # loop over each face
    for landmark in landmarks:
        mask = rotate(img=mustache, landmark=landmark)
        mask = scale(img=mask, landmark=landmark, scale=1.3)
        mask = removePadding(mask)

        if modelsize=="small":
            nose = landmark["nose_tip"][0]
        elif modelsize=="large":
            nose = landmark["nose_tip"][2]

        midpoint = (round(mask.size[0]/2), round(mask.size[1]/2.8))
        position = (nose[0] - midpoint[0], nose[1] - midpoint[1])
        img.paste(mask, position, mask)

    return img