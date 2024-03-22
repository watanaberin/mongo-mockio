from flask import Flask, flash, request, redirect, render_template
import json
from mockio.core.op import Op
from mockio.core.transformer import Transformer
from typing import List

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
        data: dict= None
        # make sure the json file in valid
        try:
            data = json.load(file)
        except:
            return render_template("index.html", hint="Invalid JSON Template, Please check your JSON file")
        
        number: int = request.form.get("number", default=100, type=int)
        if number is not None and number <= 0:
            return render_template("index.html", hint="Invalid Size, size should > 0")
        uri: str = request.form.get("uri", default='mongodb://localhost:27017', type=str)
        db: str = request.form.get("db", default='test', type=str)
        op: Op = Op(template=data, mongodb_uri=uri, db_name=db, num=number)
        if not op.client.is_connect() or not op.client.is_writable():
            return render_template("index.html", hint="MongoDB is not connectable or writable")
        
        records: List[str] = Transformer.RUN(op)
        return render_template("index.html", hint=json.dumps(data, indent=4), records=records)
    return render_template("index.html")