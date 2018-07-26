import datetime
import os

import numpy as np
import pylab as plt
import tensorflow as tf

from DataSetGenerator import DataSetGenerator
from NetworkBuilder import NetworkBuilder

def model():
    with tf.name_scope("Input") as scope:
        input_img = tf.placeholder(dtype='float', shape=[
                                None, 16, 32, 2], name="input")

    with tf.name_scope("Target") as scope:
        target_labels = tf.placeholder(
            dtype='float', shape=[None, 2], name="Targets")


    nb = NetworkBuilder()

    with tf.name_scope("ModelV2") as scope:
        model = input_img

        model = nb.attach_conv_layer(model, 16, summary=True)
        model = nb.attach_relu_layer(model)
        model = nb.attach_pooling_layer(model)

        # model = nb.attach_conv_layer(model, 32, summary=True)
        # model = nb.attach_relu_layer(model)
        # model = nb.attach_pooling_layer(model)
        # print(model.get_shape())

        # model = nb.attach_conv_layer(model, 32, summary=True)
        # model = nb.attach_relu_layer(model)
        # model = nb.attach_pooling_layer(model)
        # print(model.get_shape())

        model = nb.flatten(model)
        model = nb.attach_dense_layer(model, 200, summary=True)
        model = nb.attach_sigmoid_layer(model)
        model = nb.attach_dense_layer(model, 32, summary=True)
        model = nb.attach_sigmoid_layer(model)
        model = nb.attach_dense_layer(model, 2)
        prediction = nb.attach_softmax_layer(model)

    return input_img, target_labels, model, prediction

