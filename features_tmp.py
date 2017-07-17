import numpy as np
import os
import h5py
import argparse
from numpy import linalg as LA

from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input

ap = argparse.ArgumentParser()
ap.add_argument("-database", required = True,
	help = "Path to database which contains images to be indexed")
ap.add_argument("-index", required = True,
	help = "Name of index file")
ap.add_argument("-number", required = True,
	help = "the number of picture(150/9999)")
args = vars(ap.parse_args())

def extract_feat(img_path):
    # weights: 'imagenet'
    # pooling: 'max' or 'avg'
    # input_shape: (width, height, 3), width and height should >= 48

    input_shape = (224, 224, 3)
    model = VGG16(weights='imagenet', input_shape=(input_shape[0], input_shape[1], input_shape[2]), pooling='max',include_top=False)

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

    feats = []
    names = []

    nums = int(args["number"])

    for i, img_path in enumerate(img_list):
        if(i < nums*50 or i >= (nums+1)*50):
            continue
        norm_feat = extract_feat(img_path)
        img_name = os.path.split(img_path)[1]
        feats.append(norm_feat)
        names.append(img_name)
        print "extracting feature from image No. %d , %d images in total" % ((i + 1), len(img_list))

    feats = np.array(feats)
    # directory for storing extracted features
    output = args["index"]

    if(nums == 0):
	print(feats.shape)
	h5f = h5py.File(output,'a')	
        dataset_1 = h5f.create_dataset('dataset_1', data=feats, maxshape=(None,512),chunks=True)
        dataset_2 = h5f.create_dataset('dataset_2', data=names, maxshape=(None,),chunks=True)
        print(dataset_1.shape)
	print(dataset_1.maxshape)
	h5f.close()
    else:
        h5f = h5py.File(output, 'a')
	dataset_1 = h5f['dataset_1']
	dataset_2 = h5f['dataset_2']
	print(dataset_2.shape)
	print(dataset_2.maxshape)
	dataset_1.resize([nums*50+50,512])
	dataset_2.resize([nums*50+50])
        dataset_1[nums*50:nums*50+50] = feats
        dataset_2[nums*50:nums*50+50] = names
        h5f.close()
