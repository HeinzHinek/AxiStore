# -*- coding: utf-8 -*-

from app import app
from flask import request, jsonify
from flask_login import login_required
from config import PRODUCT_IMG_PATH, PRODUCT_THUMB_IMG_PATH, IMG_EXTENSIONS, NO_PHOTO_THUMB_URL
from PIL import Image
import os
import glob


@app.route('/uploadProductImage', methods=['POST'])
@login_required
def uploadProductImage():
    result = 'NG'
    file = request.files['file']
    prod_id = request.form['prod_id']
    if file and allowed_file(file.filename.lower()) and prod_id:
        urls = getImgUrls(prod_id)
        if urls:
            last_no = urls[-1].split('_')[-1].split('.')[0]
            ext = urls[-1].split('_')[-1].split('.')[1]
            suffix = str(int(last_no) + 1) + '.' + ext
        else:
            suffix = "1." + file.filename.split('.')[-1]
        filename = PRODUCT_IMG_PATH + 'prod_' + str(prod_id) + '_' + suffix.lower()
        file.save(filename)
        result = 'OK'
    return jsonify({'result': result, 'url': filename})


@app.route('/deleteProductImage', methods=['POST'])
@login_required
def deleteProductImage():
    result = 'NG'
    path = request.form['path'] if request.form['path'] else None
    if path:
        abspath = os.path.abspath(__file__)
        abspath = abspath.split('app')[0]
        file = abspath + 'apps/AxiStore/app' + path
        os.remove(file)
        result = 'OK'
    return jsonify({'result': result})


def getImgUrls(id):
    urls = []
    for ext in IMG_EXTENSIONS:
        urls.extend(glob.glob(PRODUCT_IMG_PATH + 'prod_' + str(id) + '_' + '*' + ext))
    urls = sorted(urls)
    return urls

def getThumbUrls(url, height=100, width=100):
    try:
        filename = 'prod_' + url.split('prod_')[1]
    except IndexError:
        return NO_PHOTO_THUMB_URL
    path = PRODUCT_IMG_PATH + filename
    im = Image.open(path)
    out_path = PRODUCT_THUMB_IMG_PATH + 'thumb_' + filename.split('.')[0] + '.png'
    try:
        Image.open(out_path)
        return out_path
    except IOError:
        pass

    im.thumbnail([height, width], Image.ANTIALIAS)
    im.save(out_path, "PNG")
    return out_path


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in IMG_EXTENSIONS