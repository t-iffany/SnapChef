# import Flask class from the flask module
from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS

import tensorflow as tf
# from io import BytesIO
import base64
import numpy as np
from pathlib import Path

# create a Flask web application instance called 'app'
app = Flask(__name__)
CORS(app)

# define IMG_SIZE
IMG_SIZE = 180

# define a route for the flask server
@app.route('/')
def index():
    return 'Flask server successfully running'

# define a route to serve the favicon.ico file
@app.route('/favicon.ico')
def favicon():
    # specify the path to the favicon.ico file
    return send_from_directory(app.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# define a route to capture image
@app.route('/capture-image', methods=['POST'])
def capture_image():
    return jsonify({'result': 'Image captured successfully'})

# define a route to classify image
@app.route('/classify-image', methods=['POST'])
def classify():
    try:
        # # Check if the request is JSON
        # if request.content_type != 'application/json':
        #     return jsonify({'error': 'Invalid content type, expected application/json'}), 400

        # # Check if an image file is present in the request
        # if 'image' not in request.json:
        #     return jsonify({'error': 'No image part'}), 400


        req = request.get_json("image")
        req = req.split(',')[1]
        img_data = base64.b64decode(req)
        img_np = np.frombuffer(img_data, dtype=np.uint8)

        with open("imgToSave.jpg", "wb") as image:
            image.write(img_np)


        # convert img_np to path format for t.keras to use
        img_path = "imgToSave.jpg"

        # data = request.get_json()
        # base64_image = data.get("image")

        # # Decode the base64 image to bytes
        # image_data = base64.b64decode(base64_image)

        # # Save the image to a file (you can use a unique filename)
        # with open("uploaded_image.jpg", "wb") as image_file:
        #     image_file.write(image_data)
         
        
        
        # # access the image file from request.files
        # image_file = request.files['image']

        # # Process the image file using BytesIO
        # image = BytesIO(image_file.read())
        # print(image)

        # # Make sure the file has an allowed extension (e.g., '.jpg' or '.png')
        # allowed_extensions = {'jpg', 'jpeg', 'png'}
        # if '.' not in image.name or image.name.rsplit('.', 1)[1].lower() not in allowed_extensions:
        #     return jsonify({'error': 'Invalid file format'})





        # # Get the uploaded image file as a BytesIO object
        # image_file = request.files.get['image']

        # # Process the image file using BytesIO
        # image = BytesIO(image_file.read())
        # print(image)

        # # Get the file extension from the frontend
        # file_extension = request.form.get('extension')

        # # Check if the file extension is allowed
        # allowed_extensions = {'jpg', 'jpeg', 'png'}

        # if not file_extension or file_extension.lower() not in allowed_extensions:
        #     return jsonify({'error': 'Invalid file format'})

        from classification import classify_image

        # Read the image file and convert it to a format compatible with TensorFlow
        image_data = tf.keras.utils.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
        image_array = tf.keras.utils.img_to_array(image_data)

        # Classify the image using the classification function from classification.py
        predicted_class, confidence = classify_image(image_array)

        # convert the confidence (a NumPy array) to a Python list
        confidence = confidence.tolist()

        # Print the classification results to the console
        print(f'Predicted Class: {predicted_class}')
        print(f'Confidence: {confidence}')

        # Return the classification results as JSON
        return jsonify({'class': predicted_class, 'confidence': confidence})

    except Exception as e:
        return jsonify({'error': str(e)})

# start the Flask development server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, use_reloader=False)
