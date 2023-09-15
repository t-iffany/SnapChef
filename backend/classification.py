import tensorflow as tf
import tensorflow_datasets as tfds
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend which doesn't require a GUI


from tensorflow.keras import layers

# display the version of tensorflow
print(tf.__version__)

# load the Flowers dataset using TensorFlow Datasets
(train_ds, val_ds, test_ds), metadata = tfds.load(
    'plant_village',
    # split=['train[:80%]', 'train[80%:90%]', 'train[90%:]'],
    # split=['train[:5%]', 'train[5%:6%]', 'train[6%:7%]'], # using 5% of dataset b/c low storage
    split=['train[:1%]', 'train[1%:2%]', 'train[2%:3%]'],
    with_info=True,
    as_supervised=True,
)

# find the class names in the metadata
class_names = metadata.features['label'].names
print(class_names)

# retrieve an image from the dataset
get_label_name = metadata.features['label'].int2str

image, label = next(iter(train_ds))
# _ = plt.imshow(image)
_ = plt.title(get_label_name(label))

# display the image
# plt.show()

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

# using Keras prepocessing layers for data augmentation (instead of tf.image)

# resizing and rescaling
IMG_SIZE = 180

resize_and_rescale = tf.keras.Sequential([
  layers.Resizing(IMG_SIZE, IMG_SIZE),
  layers.Rescaling(1./127.5, offset=-1)
])

# visualize the result of applying these layers to an image
result = resize_and_rescale(image)
# _ = plt.imshow(result)
# plt.show()

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
  # plt.imshow(augmented_image[0])
  plt.axis("off")
  # plt.show()

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
# create the model - the Sequential model
num_classes = len(class_names)

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

# compile the model
# Choose the tf.keras.optimizers.Adam optimizer and tf.keras.losses.SparseCategoricalCrossentropy loss function
# To view training and validation accuracy for each training epoch, pass the metrics argument to Model.compile
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# model summary - view all the layers of the network using the Keras Model.summary method
# code below doesn't work, says model hasn't been built yet
# model.summary()   

# train the model for a few epochs with the Keras Model.fit method - I set to 2 b/c disk space
epochs=2
history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=epochs
)

loss, acc = model.evaluate(test_ds)
print("Accuracy", acc)

# visualize training results - create plots of the loss and accuracy on the training and validation sets
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
# plt.show()

# custom data augmentation layers
# both layers will randomly invert the colors in an image, according to the same probability

# create a tf.keras.layers.Lambda layer --> good way to write concise code
def random_invert_img(x, p=0.5):
  if  tf.random.uniform([]) < p:
    x = (255-x)
  else:
    x
  return x

def random_invert(factor=0.5):
  return layers.Lambda(lambda x: random_invert_img(x, factor))

random_invert = random_invert()

plt.figure(figsize=(10, 10))
for i in range(9):
  augmented_image = random_invert(image)
  ax = plt.subplot(3, 3, i + 1)
  # plt.imshow(augmented_image[0].numpy().astype("uint8"))
  plt.axis("off")
  # plt.show()

# implement a new custom layer via subclassing, which gives you more control
class RandomInvert(layers.Layer):
  def __init__(self, factor=0.5, **kwargs):
    super().__init__(**kwargs)
    self.factor = factor

  def call(self, x):
    return random_invert_img(x)

# _ = plt.imshow(RandomInvert()(image)[0])
# plt.show()

# predict on new data
# use our model to classify an image that wasn't included in the training or validation sets
sunflower_url = "https://storage.googleapis.com/download.tensorflow.org/example_images/592px-Red_sunflower.jpg"
sunflower_path = tf.keras.utils.get_file('Red_sunflower', origin=sunflower_url)

img = tf.keras.utils.load_img(
    sunflower_path, target_size=(IMG_SIZE, IMG_SIZE)
)
img_array = tf.keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0) # Create a batch

predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])

print(
    "This image most likely belongs to {} with a {:.2f} percent confidence."
    .format(class_names[np.argmax(score)], 100 * np.max(score))
)

# define a function that takes an image as input, preprocesses it, and returns the classification results
def classify_image(image):
    # Resize and rescale the image
    resized_image = tf.image.resize(image, (IMG_SIZE, IMG_SIZE))
    preprocessed_image = tf.keras.applications.inception_v3.preprocess_input(resized_image)
   
    # Make a prediction using the loaded model
    predictions = model.predict(tf.expand_dims(preprocessed_image, 0))
   
    # Process the predictions (e.g., find the class with the highest probability)
    predicted_class = class_names[np.argmax(predictions)]
    confidence = np.max(predictions)
   
    return predicted_class, confidence

