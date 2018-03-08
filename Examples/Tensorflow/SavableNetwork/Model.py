#
#
#
#
#

import tensorflow as tf

model_dir = "."
model_name = "model.ckpt"
path = model_dir + "/" + model_name

def model_fn():
	var1 = tf.get_variable(name="var1",shape=[1],initializer=tf.zeros_initializer())
	inc_var1 = var1.assign(var1 + 1)
	return inc_var1

def restore_model_fn():
	var1 = tf.get_variable(name="var1",shape=[1])
	inc_var1 = var1.assign(var1 + 1)
	return inc_var1

