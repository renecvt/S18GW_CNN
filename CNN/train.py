import datetime
import os

import numpy as np
import tensorflow as tf

from tools.DataSetGenerator import DataSetGenerator
from tools.model import model

dg = DataSetGenerator("CNN/training_data")

input_img, target_labels, model, prediction = model()

_EPOCHS = 5
_BATCH_SIZE = 54

with tf.name_scope("Optimization") as scope:
    global_step = tf.Variable(0, name='global_step', trainable=False)
    cost = tf.nn.softmax_cross_entropy_with_logits_v2(
        logits=model, labels=target_labels)
    cost = tf.reduce_mean(cost)
    tf.summary.scalar("cost", cost)

    optimizer = tf.train.AdamOptimizer().minimize(cost, global_step=global_step)


with tf.name_scope('accuracy') as scope:
    correct_pred = tf.equal(tf.argmax(prediction, 1),
                            tf.argmax(target_labels, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))



saver = tf.train.Saver()
model_save_path = "CNN/tensorboard/model/"
model_name = 'model'

def to_pred(probas):
    return [smooth(pred) for pred in probas]

def smooth(proba):
    return 0 if proba < .5 else 1

def is_certain(probas, confidence):
    return any(x >= confidence for x in probas)

with tf.Session() as sess:
    summaryMerged = tf.summary.merge_all()

    filename = "CNN/tensorboard/summary_log/run" + \
        datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%s")

    tf.global_variables_initializer().run()
    global_accuracy = 0
    global_s = 0

    if os.path.exists(model_save_path+'checkpoint'):
        saver.restore(sess, tf.train.latest_checkpoint(model_save_path))
        print("Restored checkpoint")

    writer = tf.summary.FileWriter(filename, sess.graph)

    for epoch in range(_EPOCHS):
        batches = dg.get_mini_batches(_BATCH_SIZE, validation=False)
        for imgs, labels in batches:
            error, sumOut, acu, steps, _ = sess.run([cost, summaryMerged, accuracy, global_step, optimizer],
                                                    feed_dict={input_img: imgs, target_labels: labels})
            print("epoch=", epoch + 1, "err=", error, "accuracy=", acu)
            saver.save(sess, model_save_path+model_name)

    batches = dg.get_mini_batches(_BATCH_SIZE, validation=True)
    count_true = int()
    count_false = int()

    for imgs, labels in batches:
        for index in range(len(imgs)):
            model_pred = sess.run([prediction], feed_dict={input_img: imgs})[0][index]
            if is_certain(model_pred, .53):
                smoothed = to_pred(model_pred)
                if list(labels[index]) == smoothed:
                    count_true += 1
                else:
                    count_false += 1

    print "true count", count_true
    print "false count", count_false
    total = count_false + count_true
    print "precision", float(count_true)/total
