# pylint: disable-all
import argparse
import glob
import os
import sys

import cv2
import numpy as np
import tensorflow as tf

def predict(h1, l1):
    # First, pass the path of the image
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # image_path = sys.argv[1]
    # filename = dir_path + '/' + image_path
    image_width = 32
    image_height = 16
    num_channels = 3
    images = []
    ifos_images = []

    for f in [h1, l1]:
        image = cv2.imread(f)
        image = cv2.resize(image, (image_width, image_height), 0, 0, cv2.INTER_LINEAR)
        # image = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
        image = image.astype(np.float32)
        image = np.multiply(image, 1.0/255.0)
        ifos_images.append(image)

    images.append(ifos_images[0] + ifos_images[1])
    images = np.array(images, dtype=np.uint8)
    images = images.astype('float32')
    images = np.multiply(images, 1.0/255.0)
    x_batch = images.reshape(1,  image_height, image_width, num_channels)
    # Let us restore the saved model
    sess = tf.Session()
    # Step-1: Recreate the network graph. At this step only graph is created.
    saver = tf.train.import_meta_graph('CNN/model/GW-Noise-model.meta')
    # Step-2: Now let's load the weights saved using the restore method.
    saver.restore(sess, tf.train.latest_checkpoint('CNN/model/'))

    # Accessing the default graph which we have restored
    graph = tf.get_default_graph()

    # Now, let's get hold of the op that we can be processed to get the output.
    # In the original network y_pred is the tensor that is the prediction of the network
    y_pred = graph.get_tensor_by_name("y_pred:0")

    # Let's feed the images to the input placeholders
    x = graph.get_tensor_by_name("x:0")
    y_true = graph.get_tensor_by_name("y_true:0")


    y_test_images = np.zeros((1, 2))
    # len(os.listdir('CNN/testing_data')

    # Creating the feed_dict that is required to be fed to calculate y_pred
    feed_dict_testing = {x: x_batch}
    result = sess.run(y_pred, feed_dict=feed_dict_testing)
    # result is of this format [probabiliy_of_rose probability_of_sunflower]
    print(result)
    classes = ['GW', 'Noise']
    return classes[np.argmax(result)]
