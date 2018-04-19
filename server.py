from flask import Flask, render_template, request, jsonify, Response
import uuid
import os
from  Extract_face import extract_face
import sys
from glob import glob
import logging


IMG_PATH = 'img/'

app = Flask(__name__, static_folder="img")

logger = logging.getLogger(__name__)
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'JPG']
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.before_request
def delete_old_file():
    file_array = glob(IMG_PATH + '*')
    if len(file_array) >= 10:
        file_array.sort(key=lambda x: int(os.path.getctime(x)))
        logger.info('Delete image: {}'.format(file_array[0]))
        os.remove(file_array[0])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def face_detection():
    delete_old_file()
    img = request.files['file']
    id = uuid.uuid4()
    if img and allowed_file(img.filename):
        image_path = os.path.join(IMG_PATH) + id.hex + img.filename
        img.save(image_path)
        result = extract_face(image_path)
        if result == False:
            response = jsonify({'result': "顔が検出できませんでした"})
            response.status_code = 200
            return response
        response = jsonify(result)
        response.status_code = 200

        return response
    else:
        response = jsonify({'result': 'ファイルの形式が不正です'})
        response.status_code = 401
        return response

if __name__ == "__main__":
    port = int(sys.argv[1])
    app.run(debug=False, host='0.0.0.0', port=port)
