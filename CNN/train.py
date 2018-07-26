import datetime
import os

import numpy as np
import tensorflow as tf
import time

from tools.DataSetGenerator import DataSetGenerator
from tools.model import model

dg = DataSetGenerator("CNN/training_data")

input_img, target_labels, model, prediction = model()

_EPOCHS = 10
_BATCH_SIZE = 54

with tf.name_scope("Optimization") as scope:
    global_step = tf.Variable(0, name='global_step', trainable=False)
    cost = tf.nn.softmax_cross_entropy_with_logits_v2(
        logits=model, labels=target_labels)
    cost = tf.reduce_mean(cost)

    optimizer = tf.train.AdamOptimizer().minimize(cost, global_step=global_step)


with tf.name_scope('accuracy') as scope:
    correct_pred = tf.equal(tf.argmax(prediction, 1),
                            tf.argmax(target_labels, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

with tf.name_scope('auc') as scope:
    auc_value, _ = tf.metrics.auc(tf.argmax(target_labels, 1), tf.argmax(prediction, 1), curve='ROC')

saver = tf.train.Saver()
model_save_path = "CNN/tensorboard/model/"
model_name = 'model'

tf.summary.scalar('loss', cost)
tf.summary.scalar('accuracy', accuracy)
tf.summary.scalar('auc', auc_value)

with tf.Session() as sess:
    summaryMerged = tf.summary.merge_all()

    filename = "CNN/tensorboard/summary_log/run" + \
        datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%s")

    filename_val = "CNN/tensorboard/validation/run" + \
        datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%s")

    tf.global_variables_initializer().run()
    tf.local_variables_initializer().run()
    # if os.path.exists(model_save_path+'checkpoint'):
    #     saver.restore(sess, tf.train.latest_checkpoint(model_save_path))
    #     print("Restored checkpoint")

    writer = tf.summary.FileWriter(filename, sess.graph)
    writer1 = tf.summary.FileWriter(filename_val)

    import pylab as plt

    for epoch in range(_EPOCHS):
        train_accuracy = 0
        count = 0
        start_time = time.time()
        batches = dg.get_mini_batches(_BATCH_SIZE, validation=False)
        for imgs, labels in batches:
            error, sumOut, acu, steps, _, _= sess.run([cost, summaryMerged, accuracy, global_step, optimizer, auc_value],
                                                    feed_dict={input_img: imgs, target_labels: labels})
            print("err=", error, "accuracy=", acu)
            train_accuracy += acu
            count += 1
            writer.add_summary(sumOut, steps)
            saver.save(sess, model_save_path+model_name)

        train_accuracy /= count
        imgs, labels = dg.get_validation_images()
        summ, vali_accuracy, auc = sess.run([summaryMerged, accuracy, auc_value], feed_dict={input_img: imgs, target_labels: labels})
        writer1.add_summary(summ, epoch)

        end_time = time.time()

        print("Epoch "+str(epoch+1)+" completed : Time usage "+str(int(end_time-start_time))+" seconds")
        print("\tAccuracy:")
        print ("\t- Training Accuracy:\t{}".format(train_accuracy))
        print ("\t- Validation Accuracy:\t{}".format(vali_accuracy))


