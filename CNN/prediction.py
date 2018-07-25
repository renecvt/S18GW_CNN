# pylint: disable-all
import argparse
import glob
import os
import sys

import cv2
import numpy as np
import tensorflow as tf

from tools.DataSetGenerator import read_and_convert

def prediction(H1, L1):


    img1 = read_and_convert(H1)
    img2 = read_and_convert(L1)
    # cv2.imwrite('out1.png', img1)
    # cv2.imwrite('out2.png', img2)

    img = np.array([img1, img2])

    with tf.Session() as sess:
        saver = tf.train.import_meta_graph('./tensorboard/model/model.meta')
        saver.restore(sess, "./tensorboard/model/model")
        graph = tf.get_default_graph()

        y_pred = graph.get_tensor_by_name("ModelV2/Activation_5/y_pred:0")
        input_img = graph.get_tensor_by_name("Input/input:0")

        feed_dict_testing = {input_img: [img]}
        result = sess.run(y_pred, feed_dict=feed_dict_testing) [0]
        classes = ['Noise', 'GW']

        print
        print("Noise: {0}%  GW: {1}%".format(result[0]*100, result[1]*100))
        print "Prediction: %s" % classes[np.argmax(result)]
        return classes[np.argmax(result)]


# GW
# H1 = "/Users/karenggv/Desktop/Projects/Delfin/S18GW_CNN/CNN/training_data/GW/71/RD_Strain_H1_Template_71.png"
# L1 = "/Users/karenggv/Desktop/Projects/Delfin/S18GW_CNN/CNN/training_data/GW/71/RD_Strain_L1_Template_71.png"
# prediction(H1, L1)

# Noise
# H1 = "/Users/karenggv/Desktop/Projects/Delfin/S18GW_CNN/CNN/training_data/Noise/8/RD_Strain_H1_noise_8.png"
# L1 = "/Users/karenggv/Desktop/Projects/Delfin/S18GW_CNN/CNN/training_data/Noise/8/RD_Strain_L1_noise_8.png"
# prediction(H1, L1)
