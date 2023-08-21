# importing libraries
import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
import tensorflow as tf

from tensorflow import keras
from keras import layers
from keras.models import Sequential

# import dataset
import pathlib

dataset_url = "http://data.vision.ee.ethz.ch/cvl/food-101.tar.gz"
data_dir = tf.keras.utils.get_file('food-101', origin=dataset_url, untar=True)
data_dir = pathlib.Path(data_dir)

# count total num of images: 101,000
image_count = len(list(data_dir.glob('*/*.jpg')))
# print(image_count)

# outputting images
# bruschetta = list(data_dir.glob('bruschetta/*'))
# PIL.Image.open(str(bruschetta[0])).show()

# TRAINING
# defining parameters for the loader
batch_size = 32
img_height = 180
img_width = 180

# training split
train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir, 
    validation_split=0.2, 
    subset="training", 
    seed=123, 
    image_size=(img_height, img_width), 
    batch_size=batch_size
    )

# testing/validation split
val_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size
)

# check class names
class_names = train_ds.class_names
# print(class_names)

# visualising the datasets
plt.figure(figsize=(10, 10))

for images, labels in train_ds.take(1):
    for i in range(25):
        ax = plt.subplot(5, 5, i + 1)
        plt.imshow(images[i].numpy().astype("uint8"))
        plt.title(class_names[labels[i]])
        plt.axis("off")
    plt.show()

for image_batch, labels_batch in train_ds:
    print(image_batch.shape)
    print(labels_batch.shape)

    # convert tensors to a numpy.ndarray
    image_batch.numpy()
    labels_batch.numpy()
    break

# CONFIGURE FOR PERFORMANCE
AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# standardize the data (RGB is 0-255, which is a large value, not ideal for neural networks)
normalization_layer = layers.experimental.preprocessing.Rescaling(1./255)

# CREATING A CNN (Convolutional Neural Network) model
num_classes = len(class_names)

model = Sequential([
  layers.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
  layers.Conv2D(16, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(32, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(64, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Flatten(),
  layers.Dense(128, activation='relu'),
  layers.Dense(num_classes)
])

# compile the model
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# model summary
model.summary()

# TRAIN THE MODEL FOR 5 EPOCHS
epochs = 5
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs
)
print(history)