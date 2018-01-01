from flask import Flask, render_template, request, jsonify, Response
import uuid
import os
from  Extract_face import extract_face

IMG_PATH = 'img/'

app = Flask(__name__, static_folder="img")
print(app.url_map)

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'JPG']
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def face_detection():
    img = request.files['file']
    print(img)
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
    app.run(debug=True)
