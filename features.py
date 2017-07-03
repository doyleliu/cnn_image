import numpy as np
import os
import h5py
import argparse

from numpy import linalg as LA

from keras.applications.vgg19 import VGG19
from keras.preprocessing import image
from keras.applications.vgg19 import preprocess_input

ap = argparse.ArgumentParser()
ap.add_argument("-database", required = True,
	help = "Path to database which contains images to be indexed")
ap.add_argument("-index", required = True,
	help = "Name of index file")
args = vars(ap.parse_args())

def extract_feat(img_path):
    # weights: 'imagenet'
    # pooling: 'max' or 'avg'
    # input_shape: (width, height, 3), width and height should >= 48

    input_shape = (224, 224, 3)
    model = VGG19(weights='imagenet', input_shape=(input_shape[0], input_shape[1], input_shape[2]), pooling='max',include_top=False)

    img = image.load_img(img_path, target_size=(input_shape[0], input_shape[1]))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    feat = model.predict(img)
    norm_feat = feat[0] / LA.norm(feat[0])
    return norm_feat

def get_imlist(path):
    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.jpg')]


if __name__ == "__main__":

    db = args["database"]
    img_list = get_imlist(db)

    print "--------------------------------------------------"
    print "         feature extraction starts"
    print "--------------------------------------------------"

    feats = []
    names = []

    for i, img_path in enumerate(img_list):
        norm_feat = extract_feat(img_path)
        img_name = os.path.split(img_path)[1]
        feats.append(norm_feat)
        names.append(img_name)
        print "extracting feature from image No. %d , %d images in total" % ((i + 1), len(img_list))

    feats = np.array(feats)
    # directory for storing extracted features
    output = args["index"]

    print "--------------------------------------------------"
    print "      writing feature extraction results ..."
    print "--------------------------------------------------"

    h5f = h5py.File(output, 'w')
    h5f.create_dataset('dataset_1', data=feats)
    h5f.create_dataset('dataset_2', data=names)
    h5f.close()