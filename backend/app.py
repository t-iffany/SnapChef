# import Flask class from the flask module
from flask import Flask, send_from_directory

# create a Flask web application instance called 'app'
app = Flask(__name__)

# define a route for the flask server
@app.route('/')
def index():
    return 'Flask server successfully running'

# define a route to serve the favicon.ico file
@app.route('/favicon.ico')
def favicon():
    # specify the path to the favicon.ico file
    return send_from_directory(app.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')
  
# start the Flask development server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, use_reloader=False)
