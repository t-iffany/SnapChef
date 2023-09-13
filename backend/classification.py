import tensorflow as tf
import tensorflow_datasets as tfds
import numpy as np
import matplotlib.pyplot as plt

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