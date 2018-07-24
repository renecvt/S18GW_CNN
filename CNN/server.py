import os
from base64 import b64encode, b64decode
from flask import Flask, redirect, request, url_for, json, send_file
from flask_uploads import UploadSet, configure_uploads
from werkzeug.utils import secure_filename
from GW_predict import predict

UPLOAD_FOLDER = 'CNN/Files'
ALLOWED_EXTENSIONS = set(['txt', 'csv', 'png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["DEBUG"] = True

def allowed_file(filename):
    ext = '.' in filename and \
           filename.rsplit('.', 1)[1].lower()
    return ext, ext in ALLOWED_EXTENSIONS

@app.route('/status', methods=['GET'])
def status():
    return create_response({ 'online': True, 'message': 'UP AND RUNNING @ 1333' }, 200)

@app.route('/uploadFile', methods=['POST'])
def upload_file():
    
    # Getting a dictionary out of the JSON request
    json_request = request.get_json()

    # Verifying if the keys needed are present in request
    h1 = json_request['h1'] if 'h1' in json_request else None
    l1 = json_request['l1'] if 'l1' in json_request else None

    # Returning error if keys needed are not part of the request
    if h1 is None or l1 is None:
        return create_response({'result': False, 'message': 'File missing'}, 422)

    # Getting the extension name of the file uploaded
    h1_ext, _ = allowed_file(h1)
    l1_ext, _ = allowed_file(l1)

    # Checking if the file extension is part of the allowed extensions
    if h1_ext in ALLOWED_EXTENSIONS and l1_ext in ALLOWED_EXTENSIONS:
        result = predict(h1, l1)
        return create_response({'result': True, 'prediction': result}, 200)
    else:
        return create_response({'result': False, 'message': 'File not allowed'}, 422)

def create_response(message, status):
    response = app.response_class(
        response= json.dumps(message),
        status= status,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='1333')
