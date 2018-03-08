#
#
#
#
#

import tensorflow as tf
import Model

model = Model.model_fn()
saver = tf.train.Saver()

with tf.Session() as sess:
	#Load the model and run it
	saver.restore(sess,Model.path)

	sess.run(model)

	#Re-save the network
	saver.save(sess,Model.path)

