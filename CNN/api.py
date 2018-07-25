import os
from base64 import b64encode, b64decode
from flask import Flask, redirect, request, url_for, json
from flask_uploads import UploadSet, configure_uploads
from werkzeug.utils import secure_filename
from flask import send_file
from prediction import prediction

UPLOAD_FOLDER = 'CNN/Files'
ALLOWED_EXTENSIONS = set(['txt', 'csv', 'png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["DEBUG"] = True

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploadFile', methods=['POST'])
def upload_file():
    if 'h1' not in request.files or 'l1' not in request.files:
        return create_response({'result': False, 'message': 'File missing'}, 422)

    h1_file = request.files['h1']
    l1_file = request.files['l1']

    if h1_file.filename == '' or l1_file.filename == '':
        return create_response({'result': False, 'message': 'File missing'}, 422)
    if h1_file and l1_file and allowed_file(h1_file.filename) and allowed_file(l1_file.filename):
        h1_filename = secure_filename(h1_file.filename)
        l1_filename = secure_filename(l1_file.filename)
        h1 = os.path.join(app.config['UPLOAD_FOLDER'], h1_filename)
        l1 = os.path.join(app.config['UPLOAD_FOLDER'], l1_filename)
        h1_file.save(h1)
        l1_file.save(l1)
        # img = b64encode((open(img, "rb").read()))
        result = prediction(h1, l1)
        return create_response({'result': True, 'prediction': result}, 200)

    return create_response({'result': False, 'message': 'No allowed file'}, 422)

def create_response(message, status):
    response = app.response_class(
        response= json.dumps(message),
        status= status,
        mimetype='application/json'
    )
    return response

app.run()