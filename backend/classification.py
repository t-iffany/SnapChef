import tensorflow as tf
import tensorflow_datasets as tfds
import numpy as np
import matplotlib.pyplot as plt

from tensorflow.keras import layers

# display the version of tensorflow
print(tf.__version__)

# load the Flowers dataset using TensorFlow Datasets
(train_ds, val_ds, test_ds), metadata = tfds.load(
    'tf_flowers',
    # split=['train[:80%]', 'train[80%:90%]', 'train[90%:]'],
    split=['train[:5%]', 'train[5%:6%]', 'train[6%:7%]'], # using 5% of dataset b/c low storage
    with_info=True,
    as_supervised=True,
)

# find the class names in the metadata
class_names = metadata.features['label'].names
print(class_names)

# retrieve an image from the dataset
get_label_name = metadata.features['label'].int2str

image, label = next(iter(train_ds))
_ = plt.imshow(image)
_ = plt.title(get_label_name(label))

# display the image
plt.show()

# define parameters for the loader
batch_size = 32

# buffer preteching: when loading data, use: Dataset.cache and Dataset.prefetchAUTOTUNE = tf.data.AUTOTUNE
AUTOTUNE = tf.data.AUTOTUNE

# batch, shuffle, and configure the training, validation, and test sets for performance
def configure_for_performance(ds):
  ds = ds.cache()
  ds = ds.shuffle(buffer_size=1000)
  ds = ds.batch(batch_size)
  ds = ds.prefetch(buffer_size=AUTOTUNE)
  return ds

# train_ds = configure_for_performance(train_ds)
# val_ds = configure_for_performance(val_ds)
# test_ds = configure_for_performance(test_ds)

# use Keras prepocessing layers

# resizing and rescaling
IMG_SIZE = 180

resize_and_rescale = tf.keras.Sequential([
  layers.Resizing(IMG_SIZE, IMG_SIZE),
  layers.Rescaling(1./127.5, offset=-1)
])

# visualize the result of applying these layers to an image
result = resize_and_rescale(image)
_ = plt.imshow(result)
plt.show()

# verify that the pixels are in the [-1, 1] range
print("Min and max pixel values:", result.numpy().min(), result.numpy().max())

# data augmentation

# create a few preprocessing layers and apply them repeatedly to the same image
data_augmentation = tf.keras.Sequential([
  layers.RandomFlip("horizontal_and_vertical"),
  layers.RandomRotation(0.2),
])

# Add the image to a batch.
image = tf.cast(tf.expand_dims(image, 0), tf.float32)

plt.figure(figsize=(10, 10))
for i in range(9):
  augmented_image = data_augmentation(image)
  ax = plt.subplot(3, 3, i + 1)
  plt.imshow(augmented_image[0])
  plt.axis("off")
  plt.show()

# apply the preprocessing layers to the datasets
# data augmentation should only be applied to the training set

def prepare(ds, shuffle=False, augment=False):
  # Resize and rescale all datasets.
  ds = ds.map(lambda x, y: (resize_and_rescale(x), y), 
              num_parallel_calls=AUTOTUNE)

  if shuffle:
    ds = ds.shuffle(1000)

  # Batch all datasets.
  ds = ds.batch(batch_size)

  # Use data augmentation only on the training set.
  if augment:
    ds = ds.map(lambda x, y: (data_augmentation(x, training=True), y), 
                num_parallel_calls=AUTOTUNE)

  # Use buffered prefetching on all datasets.
  return ds.prefetch(buffer_size=AUTOTUNE)

train_ds = prepare(train_ds, shuffle=True, augment=True)
val_ds = prepare(val_ds)
test_ds = prepare(test_ds)

# train a simple model using the datasets we just prepared
# the Sequential model
num_classes = 5

model = tf.keras.Sequential([
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

# Choose the tf.keras.optimizers.Adam optimizer and tf.keras.losses.SparseCategoricalCrossentropy loss function
# To view training and validation accuracy for each training epoch, pass the metrics argument to Model.compile
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# train for a few epochs - default 5, I set to 2 b/c disk space
epochs=2
history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=epochs
)

loss, acc = model.evaluate(test_ds)
print("Accuracy", acc)