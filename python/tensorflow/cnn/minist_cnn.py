import input_data
import tensorflow as tf
from util.board import variable_summaries


#定义全局变量
flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_string('summaries_dir', './mnist_logs', 'Summaries directory')
flags.DEFINE_boolean('fake_data', False, 'If true, uses fake data '
                     'for unit testing.')
flags.DEFINE_integer('max_steps', 1000, 'Number of steps to run trainer.')
flags.DEFINE_float('learning_rate', 0.0001, 'Initial learning rate.')
flags.DEFINE_float('dropout', 0.5, 'Keep probability for training dropout.')

mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
sess = tf.InteractiveSession()

x = tf.placeholder("float", shape=[None, 784])
y_ = tf.placeholder("float", shape=[None, 10])

#权重和偏置，为避免0梯度，使用ReLU神经元，权重初始化为较小正数
def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

#卷积和池化
def conv2d(x, W):
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME') #strides:输入数据每一维的步长 padding:边界补零，'VALID'表示不可以超出边界，'SAME'表示可以超出边界

def max_pool_2x2(x):
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME') #使用最大池，即对卷积特征，选择最大的；ksize表示在各个维度的取值范围，这里使用2*2

#一层卷积权重和偏置
W_conv1 = weight_variable([5, 5, 1, 32]) #使用5*5*1的权重做特征映射，进行32次，即32个channel
variable_summaries(W_conv1, "weights_layer1")
b_conv1 = bias_variable([32])  #偏置与channel数相同
variable_summaries(b_conv1, "bias_layer1")

#将x转为cnn需要的4d向量
x_image = tf.reshape(x, [-1,28,28,1]) # -1表示图片数，有多少就表示多少

#计算出一层卷积特征
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1) #做一层卷积后28*28*1*32
h_pool1 = max_pool_2x2(h_conv1) #做池化后14*14*1*32

#二层卷积权重和偏置
W_conv2 = weight_variable([5, 5, 32, 64]) #用5*5*32做特征映射，进行64次，即64个channel
variable_summaries(W_conv2, "weights_layer2")
b_conv2 = bias_variable([64]) #偏置也为64个
variable_summaries(b_conv2, "bias_layer2")

#计算二层卷积特征
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)#二层卷积后14*14*64
h_pool2 = max_pool_2x2(h_conv2) #做池化后7*7*64

#第三层，密集连接层权重和偏置
W_fc1 = weight_variable([7 * 7 * 64, 1024])#全连接层1024个节点
variable_summaries(W_fc1, "weights_fc1")
b_fc1 = bias_variable([1024])
variable_summaries(b_fc1, "bias_fc1")

#将卷积池化后的张量转成向量，计算出经过最终特征变换得到的特征
h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64]) #二层卷积后的特征进行一维展开
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1) #全连接

#dropout 以一定的概率使某些节点输出为0
keep_prob = tf.placeholder("float")
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

#使用softmax 做分类
W_fc2 = weight_variable([1024, 10])
variable_summaries(W_fc2, "weights_fc2")
b_fc2 = bias_variable([10])
variable_summaries(b_fc2, "weights_fc2")

y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

cross_entropy = -tf.reduce_sum(y_*tf.log(y_conv))
tf.summary.scalar('cross entropy', cross_entropy)
train_step = tf.train.AdamOptimizer(FLAGS.learning_rate).minimize(cross_entropy)
#train_step = tf.train.GradientDescentOptimizer(1e-4).minimize(cross_entropy)

correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
tf.summary.scalar('accuracy', accuracy)

merged = tf.summary.merge_all()
train_writer = tf.summary.FileWriter(FLAGS.summaries_dir + '/train',
                                      sess.graph)
test_writer = tf.summary.FileWriter(FLAGS.summaries_dir + '/test')
sess.run(tf.global_variables_initializer())


def feed_dict(train):
    """Make a TensorFlow feed_dict: maps data onto Tensor placeholders."""
    if train or FLAGS.fake_data:
        xs, ys = mnist.train.next_batch(100, fake_data=FLAGS.fake_data)
        k = FLAGS.dropout
    else:
        xs, ys = mnist.test.images, mnist.test.labels
        k = 1.0
    return {x: xs, y_: ys, keep_prob: k}

for i in range(FLAGS.max_steps):
  batch = mnist.train.next_batch(50)
  if i%100 == 0:
    train_accuracy = accuracy.eval(feed_dict={
        x:batch[0], y_: batch[1], keep_prob: 1.0}) #feed_dict用于传入变量的值，变量名前面用palceholder占位，在计算时通过feed_dict传入
    #summary = sess.run(merged, feed_dict=feed_dict(False))
    #test_writer.add_summary(summary, i)
    print ("step %d, training accuracy %g"%(i, train_accuracy))
  train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

print ("test accuracy %g"%accuracy.eval(feed_dict={
    x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))

train_writer.close()
test_writer.close()