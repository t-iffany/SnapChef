# import Flask class from the flask module
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS

# create a Flask web application instance called 'app'
app = Flask(__name__)
CORS(app)

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

# start the Flask development server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, use_reloader=False)
