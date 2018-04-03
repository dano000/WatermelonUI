#
#
#
#
#

#Model Hyperparameters

AUDIO_LENGTH = 2048
DENSE_UNITS = 256
DROP_RATE = .4
LEARNING_RATE = .01
def model_fn(features,labels,mode):

	input_layer = tf.reshape(features["audio"],[-1,AUDIO_LENGTH],name="Input")

	dense = tf.layers.dense(
		inputs=input_layer,
		units=DENSE_UNITS,
		name="Dense")

	drop = tf.layers.drop(
		inputs=input_layer,
		rate=DROP_RATE,
		name="Drop")

	logits = tf.layers.dense(
		inputs=drop,
		units=2,
		name="Logits")

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