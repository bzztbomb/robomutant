#!/usr/bin/env python

from utils import Data
import model
import tensorflow as tf

# Load Training Data
data = Data()

# Start session
sess = tf.InteractiveSession()

# Learning Functions
L2NormConst = 0.001
train_vars = tf.trainable_variables()
for var in tf.trainable_variables():
    print(var.name)
loss = tf.reduce_mean(tf.square(tf.sub(model.y_, model.y, name='loss_subtract'))) #+ tf.add_n([tf.nn.l2_loss(v) for v in train_vars]) * L2NormConst
train_step = tf.train.AdamOptimizer(1e-4).minimize(loss)

sess.run(tf.global_variables_initializer())

logs_path = './logs'
summary_writer = tf.train.SummaryWriter(logs_path, graph=tf.get_default_graph())

tf.scalar_summary("loss", loss)
merged_summary_op = tf.summary.merge_all()

# Training loop variables
epochs = 100
batch_size = 50
num_samples = data.num_examples
step_size = int(num_samples / batch_size)
saver = tf.train.Saver()

for epoch in range(epochs):
    for i in range(step_size):
        batch = data.next_batch(batch_size)
        train_step.run(feed_dict={model.x: batch[0], model.y_: batch[1], model.keep_prob: 0.8})

        # if i%10 == 0:
        loss_value = loss.eval(feed_dict={model.x:batch[0], model.y_: batch[1], model.keep_prob: 1.0})
        print("epoch: %d step: %d loss: %g"%(epoch, epoch * batch_size + i, loss_value))

        summary = merged_summary_op.eval(feed_dict={model.x:batch[0], model.y_: batch[1], model.keep_prob: 1.0})
        summary_writer.add_summary(summary, epoch * batch_size + i)
    # Save the Model
    saver.save(sess, "model.ckpt")
    print("model saved")
