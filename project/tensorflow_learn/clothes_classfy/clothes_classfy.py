# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import os

def create_model():
    """定义模型

    Returns:
        [model]: 定义的模型
    """
    # 建立模型
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)), # 将图像的格式从二维数组（28 x 28像素）转换为一维数组（28 * 28 = 784像素）
        keras.layers.Dense(128, activation='relu'), # 两个神经层，第一Dense层具有128个节点（或神经元）
        keras.layers.Dense(10) # 第二层（也是最后一层）返回长度为10的logits数组
    ])

    # 编译模型
    model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

    return model

# 加载数据
fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# 数据预处理，归一化
train_images = train_images / 255.0
test_images = test_images / 255.0

# 创建一个基本的模型实例
model = create_model()

# 定义回调保存路径
checkpoint_path = "./project/tensorflow_learn/clothes_classfy/training/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# 创建一个保存模型权重的回调
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)
# 训练模型
model.fit(train_images, 
          train_labels, 
          epochs=10,
          validation_data=(test_images,test_labels),
          callbacks=[cp_callback]) # 通过回调训练

# 评估准确性
test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
print('\nTest accuracy:', test_acc)

# 保存模型
model.save('./project/tensorflow_learn/clothes_classfy/saved_model/model') 


