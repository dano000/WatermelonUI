#
#
#
#Tensorflow model for watermelon ripeness
#

import tensorflow as tf

model_type = "IMAGE"
#Model HyperParameters
IM_WIDTH = 128
IM_HEIGHT = 128
IM_CHANNELS = 1
KERNEL_SIZE = [5,5]
CONV_FILTERS = 8
POOL_STRIDE = 2
POOL_SIZE = [2,2]
DENSE_UNITS = 1024
DROP_RATE = .4
LEARNING_RATE = .01
def model_fn(features,labels,mode):

	with tf.name_scope("Input"):
		input_layer = tf.reshape(features["images"],[-1,IM_WIDTH,IM_HEIGHT,IM_CHANNELS]);


	with tf.name_scope("Convolutional"):
		conv = tf.layers.conv2d(
			input_layer,
			filters=CONV_FILTERS,
			kernel_size=KERNEL_SIZE,
			padding="same",
			activation=tf.nn.relu)
		pool = tf.layers.max_pooling2d(
			inputs=conv,
			pool_size=POOL_SIZE,
			strides = POOL_STRIDE)

	with tf.name_scope("Dense"):
		pool_flat = tf.reshape(pool,[-1,int(IM_WIDTH/POOL_STRIDE*IM_HEIGHT/POOL_STRIDE*CONV_FILTERS)])

		dense = tf.layers.dense(
			inputs=pool_flat,
			units=DENSE_UNITS,
			activation=tf.nn.relu)
		dropout = tf.layers.dropout(
			inputs =dense ,
			rate=DROP_RATE,
			training=mode == tf.estimator.ModeKeys.TRAIN)
	with tf.name_scope("Logits"):
		logits = tf.layers.dense(inputs=dropout,units=2,name="logits")

	with tf.name_scope("Predictions"):
		predictions = {
			"classes": tf.argmax(input=logits,axis=1,name="classes"),
			"probabilites":tf.nn.softmax(logits,name="softmax_tensor")
		}
	if mode == tf.estimator.ModeKeys.PREDICT:
	
		return tf.estimator.EstimatorSpec(mode=mode,predictions=predictions,
			export_outputs=outputs)

	with tf.name_scope("Loss"):
		loss = tf.losses.sparse_softmax_cross_entropy(labels=labels,logits=logits)

	if mode == tf.estimator.ModeKeys.TRAIN:
		with tf.name_scope("Optimize"):
			optimizer = tf.train.GradientDescentOptimizer(learning_rate=LEARNING_RATE)
			train_op = optimizer.minimize(
				loss = loss,
				global_step=tf.train.get_global_step())
		return tf.estimator.EstimatorSpec(mode=mode,loss=loss,train_op=train_op)

	eval_metric_ops = {
		"accuracy" : tf.metrics.accuracy( 
			labels=labels,predictions=predictions["classes"])
	}
	return tf.estimator.EstimatorSpec(mode=mode,loss=loss,eval_metric_ops=eval_metric_ops);

