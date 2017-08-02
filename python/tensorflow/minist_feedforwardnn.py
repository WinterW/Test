import input_data
import tensorflow as tf
import math
import time

data_sets = input_data.read_data_sets('MNIST_data', one_hot=True)

#定义数据
images_placeholder = tf.placeholder(tf.float32, shape=(100, 28*28)) #循环训练时，数据被切片以符合这里设置的100
labels_placeholder = tf.placeholder(tf.int32, shape=(100)) #？为啥是100

weights = tf.Variable(tf.truncated_normal([28*28, 128], stddev=1.0 / math.sqrt(float(28*28))), name='weights')
biases = tf.Variable(tf.zeros([128]), name='biases')

#定义隐藏层
# Hidden 1
with tf.name_scope('hidden1'):
    weights = tf.Variable(tf.truncated_normal([28*28, 128], stddev=1.0 / math.sqrt(float(28*28))), name='weights')
    biases = tf.Variable(tf.zeros([128]), name='biases')
    hidden1 = tf.nn.relu(tf.matmul(images_placeholder, weights) + biases)
# Hidden 2
with tf.name_scope('hidden2'):
    weights = tf.Variable(tf.truncated_normal([128, 32], stddev=1.0 / math.sqrt(float(128))), name='weights')
    biases = tf.Variable(tf.zeros([32]), name='biases')
    hidden2 = tf.nn.relu(tf.matmul(hidden1, weights) + biases)

#定义线性链接层
# Linear
with tf.name_scope('softmax_linear'):
    weights = tf.Variable(tf.truncated_normal([32, 10], stddev=1.0 / math.sqrt(float(32))), name='weights')
    biases = tf.Variable(tf.zeros([10]), name='biases')
    logits = tf.matmul(hidden2, weights) + biases

#定义损失
# batch_size = tf.size(labels)
# labels = tf.expand_dims(labels, 1)
# indices = tf.expand_dims(tf.range(0, batch_size, 1), 1)
# concated = tf.concat(1, [indices, labels])
# onehot_labels = tf.sparse_to_dense(
#     concated, tf.pack([batch_size, 10]), 1.0, 0.0)

cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits, labels_placeholder, name='xentropy')
loss = tf.reduce_mean(cross_entropy, name='xentropy_mean')

tf.scalar_summary(loss.op.name, loss)
optimizer = tf.train.GradientDescentOptimizer(0.001)
global_step = tf.Variable(0, name='global_step', trainable=False)
train_op = optimizer.minimize(loss, global_step=global_step)

with tf.Graph().as_default():
    with tf.Session() as sess:
        init = tf.initialize_all_variables()
        sess.run(init)

# for step in range(2000):
#     sess.run(train_op)
#

for step in range(2000):
    start_time = time.time()
    images_feed, labels_feed = data_sets.next_batch(100)
    feed_dict = {
        images_placeholder: images_feed,
        labels_placeholder: labels_feed,
    }
    _, loss_value = sess.run([train_op, loss],
                             feed_dict=feed_dict)
    duration = time.time() - start_time
    if step % 100 == 0:
        print ('Step %d: loss = %.2f (%.3f sec)' % (step, loss_value, duration))