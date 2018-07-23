# pylint: disable-all

import cv2
import os
import glob
from sklearn.utils import shuffle
import numpy as np


def load_train(train_path, image_width, image_height, classes):
    images = []
    labels = []
    img_names = []
    cls = []
    print('>> Reading training images <<')

    for fields in classes:
        index = classes.index(fields)
        print('Reading {} file (Index: {})'.format(fields, index))
        path = os.path.join(train_path, fields)

        for p in [name for name in os.listdir(path) if not name.startswith(".")]:
            files = glob.glob(os.path.join(path, p, '*g'))
            ifos_images = []
            for fl in files:
                image = cv2.imread(fl)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                image = cv2.resize(
                    image, (image_width, image_height), 0, 0, cv2.INTER_LINEAR)
                ifos_images.append(image)
            images.append([ifos_images[0], ifos_images[1]])
            label = np.zeros(len(classes))
            label[index] = 1.0
            labels.append(label)
            flbase = os.path.basename(fl)
            img_names.append(flbase)
            cls.append(fields)
    images = np.array(images)
    labels = np.array(labels)
    img_names = np.array(img_names)
    cls = np.array(cls)

    return images, labels, img_names, cls


class DataSet(object):

    def __init__(self, images, labels, img_names, cls):
        self._num_examples = images.shape[0]

        self._images = images
        self._labels = labels
        self._img_names = img_names
        self._cls = cls
        self._epochs_done = 0
        self._index_in_epoch = 0

    @property
    def images(self):
        return self._images

    @property
    def labels(self):
        return self._labels

    @property
    def img_names(self):
        return self._img_names

    @property
    def cls(self):
        return self._cls

    @property
    def num_examples(self):
        return self._num_examples

    @property
    def epochs_done(self):
        return self._epochs_done

    def next_batch(self, batch_size):
        """Return the next `batch_size` examples from this data set."""
        start = self._index_in_epoch
        self._index_in_epoch += batch_size

        if self._index_in_epoch > self._num_examples:
            # After each epoch we update this
            self._epochs_done += 1
            start = 0
            self._index_in_epoch = batch_size
            assert batch_size <= self._num_examples
        end = self._index_in_epoch

        return self._images[start:end], self._labels[start:end], self._img_names[start:end], self._cls[start:end]


def read_train_sets(train_path, image_width, image_height, classes, validation_size):
    class DataSets(object):
        pass
    data_sets = DataSets()

    images, labels, img_names, cls = load_train(
        train_path, image_width, image_height, classes)
    images, labels, img_names, cls = shuffle(images, labels, img_names, cls)

    if isinstance(validation_size, float):
        validation_size = int(validation_size * images.shape[0])

    validation_images = images[:validation_size]
    validation_labels = labels[:validation_size]
    validation_img_names = img_names[:validation_size]
    validation_cls = cls[:validation_size]

    train_images = images[validation_size:]
    train_labels = labels[validation_size:]
    train_img_names = img_names[validation_size:]
    train_cls = cls[validation_size:]

    data_sets.train = DataSet(
        train_images, train_labels, train_img_names, train_cls)
    data_sets.valid = DataSet(
        validation_images, validation_labels, validation_img_names, validation_cls)

    return data_sets
