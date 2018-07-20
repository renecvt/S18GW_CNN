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
    if 'h1' not in request.files or 'l1' not in request.files:
        return create_response({'result': False, 'message': 'File missing'}, 422)

    h1_file = request.files['h1']
    l1_file = request.files['l1']

    if h1_file.filename == '' or l1_file.filename == '':
        return create_response({'result': False, 'message': 'File missing'}, 422)

    h1_ext, h1res = allowed_file(h1_file.filename)
    l1_ext, l1res = allowed_file(l1_file.filename)

    if h1_file and l1_file and h1res and l1res:
        h1_filename = secure_filename(h1_file.filename)
        l1_filename = secure_filename(l1_file.filename)
        h1 = os.path.join(app.config['UPLOAD_FOLDER'], h1_filename)
        l1 = os.path.join(app.config['UPLOAD_FOLDER'], l1_filename)
        h1_file.save(h1)
        l1_file.save(l1)
        # img = b64encode((open(img, "rb").read()))
        if h1_ext == 'png' and l1_ext == 'png':
            result = predict(h1, l1)
            return create_response({'result': True, 'prediction': result}, 200)

        return create_response({'result': False, 'message': 'Images format must be png'}, 422)

    return create_response({'result': False, 'message': 'No allowed file'}, 422)

def create_response(message, status):
    response = app.response_class(
        response= json.dumps(message),
        status= status,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='1333')
