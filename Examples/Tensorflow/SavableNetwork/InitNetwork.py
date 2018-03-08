#
#
#
#
#

import tensorflow as tf
import Model

model = Model.model_fn()


init = tf.global_variables_initializer()
saver = tf.train.Saver()
with tf.Session() as sess:
	sess.run(init)
	sess.run(model)
	saver.save(sess,Model.path)

