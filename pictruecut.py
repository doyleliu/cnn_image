from PIL import Image
import os
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-database", required = True,
	help = "Path to database which contains images to be indexed")
args = vars(ap.parse_args())

def get_imlist(path):
    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.jpg')]

if __name__ == "__main__":
    db = args["database"]
    img_list = get_imlist(db)
    for i, img_path in enumerate(img_list):
        im = Image.open(img_path)
        (x,y) = im.size #read image size
        x_s = 224 #define standard width
        y_s = 224 #calc height based on standard width
        out = im.resize((x_s,y_s),Image.ANTIALIAS) #resize image with high-quality
        out.save(img_path)
