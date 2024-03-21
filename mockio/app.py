import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import json
from .utils.op import Op
from .utils.transformer import Transformer
import mockio
from typing import Union
app = Flask(__name__)

ALLOWED_EXTENSIONS = {'json'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        data = json.load(file)
        number: Union[int, None] = request.form.get("number", type=int)
        uri: Union[int, None] = request.form.get("text", type=str)
        op: Op = Op(data, uri, number)
        Transformer.RUN(op)
        return render_template("index.html", file_content=data)
    return render_template("index.html")