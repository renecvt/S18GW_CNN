import pickle
from os import listdir
from os.path import isfile, join
from random import shuffle

import cv2
import numpy as np
import imutils

def read_and_convert(path, image_size=(16, 32)):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = img.shape[:2]
    sh, sw = image_size

    aspect = w/h

    if aspect < 1: # vertical image
        new_img = imutils.rotate_bound(img, 90)
    else:
        new_img = img.copy()

    img = cv2.resize(new_img, (sw, sh), 0, 0, cv2.INTER_LINEAR)
    return img

class DataSetGenerator:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.data_labels = self.get_data_labels()
        self.data_info, self.validation, self.train = self.get_data_paths()

    def get_data_labels(self):
        data_labels = []
        for filename in listdir(self.data_dir):
            if not isfile(join(self.data_dir, filename)):
                data_labels.append(filename)
        return data_labels

    def get_data_paths(self):
        data_paths = []

        for label in self.data_labels:
            img_lists = []
            path = join(self.data_dir, label)

            folders = [p for p in listdir(path) if not p.startswith(".")]

            for folder in folders:
                file_path = join(path, folder)
                images = []
                for filename in [p for p in listdir(file_path) if not p.startswith(".")]:
                    image_path = join(file_path, filename)
                    images.append(image_path)
                img_lists.append(images)
            shuffle(img_lists)
            data_paths.append(img_lists)

        validation_size_noise = int(0.2 * len(data_paths[0]))
        validation_size_gw = int(0.2 * len(data_paths[1]))

        validation_paths = [data_paths[0][:validation_size_noise], data_paths[1][:validation_size_gw]]
        train_paths = [data_paths[0][validation_size_noise:], data_paths[1][validation_size_gw:]]

        return data_paths, validation_paths, train_paths

    def save_labels(self, path):
        pickle.dump(self.data_labels, open(path, "wb"))

    def get_validation_images(self):
        images = []
        labels = []
        paths = self.validation
        for i in range(len(self.data_labels)):
            label = np.zeros(len(self.data_labels), dtype=int)
            label[i] = 1
            for p in paths[i]:
                img1 = read_and_convert(p[0])
                img2 = read_and_convert(p[1])
                arr = np.array([img1, img2])
                arr = arr.reshape(16, 32, 2)
                images.append(arr)
                labels.append(label)

        return np.array(images, dtype=np.uint8), np.array(labels, dtype=np.uint8)

    def get_mini_batches(self, batch_size=10, image_size=(16, 32), validation = False):
        images = []
        labels = []
        empty = False
        counter = 0
        paths = self.validation if validation else self.train
        each_batch_size = int(batch_size/len(paths))
        while True:
            for i in range(len(self.data_labels)):
                label = np.zeros(len(self.data_labels), dtype=int)
                label[i] = 1
                if len(paths[i]) < counter+1:
                    empty = True
                    continue
                empty = False
                img1 = read_and_convert(paths[i][counter][0])
                img2 = read_and_convert(paths[i][counter][1])
                arr = np.array([img1, img2])
                arr = arr.reshape(16, 32, 2)
                images.append(arr)
                labels.append(label)
            counter += 1

            if empty:
                break

            if (counter) % each_batch_size == 0:
                yield np.array(images, dtype=np.uint8), np.array(labels, dtype=np.uint8)
                del images
                del labels
                images = []
                labels = []




