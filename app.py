from flask import Flask, jsonify, request
from s3 import write_image_to_s3, get_image_from_s3, upload_image_to_s3
from rekognition import detect_labels
from opencv import grab_cut, unsharp_mask, decode_image
from config import BUCKET
import time

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"message": "Hello World!"})


@app.route('/search/<file_name>')
def search(file_name):
    s3_image = get_image_from_s3(file_name)
    image = decode_image(s3_image)

    sharpened_image = unsharp_mask(image)
    grab_cut_image = grab_cut(sharpened_image)

    dest_path = '/grab-cut/' + file_name
    write_image_to_s3(grab_cut_image, BUCKET, dest_path)

    labels = detect_labels(dest_path)

    result = list(map(lambda label: label['Name'], labels))
    return jsonify(result)


@app.route('/sharpen', methods=['POST'])
def sharpen_labels():
    file = request.files["image"]
    key = str(time.time()) + file.filename
    upload_image_to_s3(file, '/sharpen/before-'+key)

    s3_image = get_image_from_s3('/sharpen/before-'+key)
    image = decode_image(s3_image)

    sharpen_image = unsharp_mask(image)
    write_image_to_s3(sharpen_image, BUCKET, '/sharpen/after-'+key)
    labels = detect_labels('/sharpen/after-'+key)
    # print(labels)
    result = list(map(lambda label: label['Name'], labels))
    return jsonify(result)

@app.route('/grabcut', methods=['POST'])
def grab_cut_labels():
    file = request.files["image"]
    key = str(time.time()) + file.filename
    before_prefix = '/grabcut/before-'
    after_prefix = '/grabcut/after'
    upload_image_to_s3(file, before_prefix + key)

    s3_image = get_image_from_s3(before_prefix + key)
    image = decode_image(s3_image)

    grab_cut_image = grab_cut(image)
    write_image_to_s3(grab_cut_image, BUCKET, after_prefix+key)
    labels = detect_labels(after_prefix+key)

    result = list(map(lambda label: label['Name'], labels))
    return jsonify(result)


def sharpen_grab_cut_labels():
    return jsonify()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
