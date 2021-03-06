import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import flask
from app import *
from subprocess import Popen, PIPE, STDOUT
import subprocess

# Initialize the Flask application
app = Flask(__name__, static_url_path='/McHacks/webui/static')

bash = """mv /upload/test.md ../
fluidsynth -F output.wav font.sf2 test.mid
lame --preset standard output.wav test.mp3
chmod 755 test.mp3
rm /static/test.mp3
mv test.mp3 static"""

#APP_ROOT = os.path.dirname(os.path.abspath(__file__))
#UPLOAD_FOLDER = os.path.join(APP_ROOT, '/upload')
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'upload'
app.config['STATIC_FOLDER'] = '/McHacks/webui/static'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['midi', 'mid'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return render_template('index.html')


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        try:
            r=RandomGenerator("./upload/" +str(filename))
            r.writeMidToFile()
        except:
            return render_template('error.html')
        subprocess.Popen(["bash", "-c", bash])
        return render_template('player.html')
    else:
        return render_template('error.html')
	

	        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        #return redirect(url_for('uploaded_file',#filename=filename))


# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload 
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
                               
@app.route('/static/<filename>')
def static_file(filename):
    return app.send_static_file(app.config['STATIC_FOLDER'])


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("8083"),
        debug=True
    )

