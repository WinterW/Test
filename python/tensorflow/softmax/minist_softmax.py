import input_data
import tensorflow as tf
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

#训练数据feature占位
x = tf.placeholder(tf.float32, [None, 784])

#权重和偏置变量
W = tf.Variable(tf.zeros([784, 10])) #实际是权重的转置
b = tf.Variable(tf.zeros([10]))

#定义softmax模型
y = tf.nn.softmax(tf.matmul(x,W) + b) #x W顺序不可变

#训练数据label占位
y_ = tf.placeholder("float", [None,10])

#定义交叉熵，即优化目标
cross_entropy = -tf.reduce_sum(y_*tf.log(y))

#使用梯度下降法，最小化交叉熵
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

init = tf.global_variables_initializer()
sess = tf.Session() #未设置graph,使用默认图
sess.run(init)

#每次取100条数据，进行随机梯度下降训练
for i in range(1000):
  batch_xs, batch_ys = mnist.train.next_batch(100)
  sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

#方差进行模型评估
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1)) #预测值1的索引和实际值1的索引是否相同
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float")) #bool转浮点型，计算平均值，即正确率
print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))