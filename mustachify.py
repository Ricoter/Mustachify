from PIL import Image, ImageDraw
from face_recognition import load_image_file, face_landmarks

def mustachify(img_file, mustache_file="mustache.png"):
    # load file to img
    img_array = load_image_file(img_file)
    # get landmarks of all faces
    landmarks = face_landmarks(img_array)
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