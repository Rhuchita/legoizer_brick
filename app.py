from flask import Flask, render_template, flash, request, redirect, url_for
import legofy
#import os

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/uploadimage', methods=['GET', 'POST'])
def uploader():
    if request.method == "POST":
        global imagereq
        imagereq = request.files['image']
        passpath = "uploads/"+imagereq.filename
        imgpath = "static/"+passpath
        imagereq.save(imgpath)
        imagelego = legofy.main(imgpath, size=30)
        legoname = imagereq.filename
        legos, legoext = map(str, legoname.split("."))
        legofn = legos+"_lego.png"
        legopath = "uploads/"+legofn
        return render_template('legofy.html', imagepath=legopath)


if __name__ == '__main__':
    app.run(debug=True)
