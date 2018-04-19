import cv2
from PIL import Image
from keras.preprocessing.image import load_img, img_to_array
from settings import CHECK_CATEGORY
import train
import numpy as np
import argparse
import glob
import os
import time

CASCADE_PATH = os.environ["CV2_CASCADE_FILE_PATH"]
cascade = cv2.CascadeClassifier(CASCADE_PATH)
color = (255, 255, 255)
image_size = 32

def extract_face(image_path):
    print('Extract face...')
    image = cv2.imread(image_path)
    facerect = cascade.detectMultiScale(image, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))
    frontalface_path = "{}frontalface.png".format(image_path)
    cv2.imwrite(frontalface_path, image)
    os.remove(image_path)
    img = cv2.imread(frontalface_path)
    print(len(facerect))
    if len(facerect) == 0:
        return False
    for rect in facerect:
        cv2.rectangle(image, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), color, thickness=2)
        x = rect[0]
        y = rect[1]
        width = rect[2]
        height = rect[3]
        dst = img[y:y + height, x:x + width]
        output_path = "{}out.png".format(image_path)
        cv2.imwrite(output_path, dst)
        os.remove(frontalface_path)
        cv2.imread(output_path)
        X = []

        img = load_img(output_path, target_size=(image_size, image_size))
        in_data = img_to_array(img)
        X.append(in_data)
        X = np.array(X)
        X = X.astype("float") / 256

        model = train.build_model(X.shape[1:])
        model.load_weights("face-model2.h5py")
        print('model predict start')

        pre = model.predict(X)
        print(pre)
        if pre[0][0] > pre[0][1]:
            result = {
                "result": CHECK_CATEGORY[0],
                "score": str(pre[0][0]),
                "img_url": output_path
            }
            return result
        else:
            result = {
                "result": CHECK_CATEGORY[1],
                "score": str(pre[0][1]),
                "img_url": output_path
            }
            return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='clip face-image from imagefile and do data argumentation.')
    parser.add_argument('-p', required=True, help='set files path.', metavar='imagefile_path')
    args = parser.parse_args()
    img = Image.open(args.p)
    extract_face(args.p)
