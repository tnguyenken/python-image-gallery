import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

from ..aws import s3
import urllib.parse

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

S3_IMAGE_BUCKET = 'edu.au.cc.image-gallery-config1'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(username):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            s3.put_object(bucket_name=S3_IMAGE_BUCKET+'.'+username, key=username, value=filename)
            #s3.put_object(username=username, bucket_name=$S3_IMAGE_BUCKET, key=username, value=filename) 
            return redirect('/upload_file/' + urllib.parse.quote(username))
