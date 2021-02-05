from PIL import Image, ImageDraw
from face_recognition import load_image_file, face_landmarks

def mustachify(img_file):
    img_array = load_image_file(img_file)
    landmarks = face_landmarks(img_array)
    img = Image.fromarray(img_array)
    draw = ImageDraw.Draw(img)
    mustache = Image.open("mustache.png")
    for face in landmarks:
        xmouth = list(zip(*face["top_lip"]))[0]
        mouthwidth = max(xmouth) - min(xmouth)
        x, y = mustache.size
        ratio = mouthwidth / x * 2
        mask = mustache.resize((int(x*ratio)+1, int(y*ratio)+1))
        pos = face["nose_tip"][0][0]-int(mouthwidth/1.4), face["nose_tip"][0][1] - int(mouthwidth/4)
        img.paste(mask, pos, mask)
    return img