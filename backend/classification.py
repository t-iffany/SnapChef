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

train_ds = configure_for_performance(train_ds)
val_ds = configure_for_performance(val_ds)
test_ds = configure_for_performance(test_ds)

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

# verify that the pixels are in the [-1, 1] range
print("Min and max pixel values:", result.numpy().min(), result.numpy().max())