# -*- coding: utf-8 -*-

from app import app
from flask import request, jsonify
from flask_login import login_required
from config import PRODUCT_IMG_PATH, IMG_EXTENSIONS
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
        filename = PRODUCT_IMG_PATH + 'prod_' + str(prod_id) + '_' + suffix
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
        file = abspath + 'app' + path
        os.remove(file)
        result = 'OK'
    return jsonify({'result': result})


def getImgUrls(id):
    urls = []
    for ext in IMG_EXTENSIONS:
        urls.extend(glob.glob(PRODUCT_IMG_PATH + 'prod_' + str(id) + '*' + ext))
    urls = sorted(urls)
    return urls

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in IMG_EXTENSIONS