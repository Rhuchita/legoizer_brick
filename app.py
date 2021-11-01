from flask import Flask, render_template, flash, request, redirect, url_for
import legofy
from PIL import Image
#import os

app = Flask(__name__)


def color_palette(mode):
    if mode == "solid":
        return ("#fec400", "#e76318", "#de000d", "#de378b", "#0057a8", "#ffff99", "#ee9dc3", "#87c0ea", "#f49b00", "#9c006b", "#478cc6",
                "#5e748c", "#80081b", "#2c1577", "#002541", "#007b28", "#009624", "#5f8265", "#003416", "#95b90b", "#5b1c0c", "#d9bb7b",
                "#8d7452", "#aa7d55", "#300f06", "#d67240", "#f5c189", "#a83d15", "#f4f4f4", "#e4e4da", "#9c9291", "#4c5156", "#010101")
    elif mode == "transparent":
        return ("#f9ef69", "#ec760e", "#e76648", "#e02a29", "#ee9dc3", "#9c95c7", "#b6e0ea",
                "#50b1e8", "#cee3f6", "#63b26e", "#99ff66", "#faed5b", "#a69182", "#eeeeee")
    elif mode == "effects":
        return ("#8d9496", "#aa7f2e", "#493f3b", "#fefcd5")
    else:
        return "1,2,3,4,5,6,7"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/legofied', methods=['GET', 'POST'])
def uploader():
    if request.method == "POST":
        global imagereq
        imagereq = request.files['image']
        passpath = "uploads/"+imagereq.filename
        imgpath = "static/"+passpath
        imagereq.save(imgpath)

        nosize = int(request.form['bricksize'])
        palettes = request.form.get('palettetype').lower()
        dithert = request.form.get('dither').lower()

        images = Image.open(imagereq)
        width = images.size[0]
        height = images.size[1]
        brsize = int(max(width, height)/nosize)

        imagelego = legofy.main(imgpath, palette_mode=palettes,
                                size=brsize, dither=dithert)
        legoname = imagereq.filename
        legos, legoext = map(str, legoname.split("."))
        legofn = legos+"_lego.png"
        legopath = "uploads/"+legofn

        selected_palette = color_palette(palettes)
        return render_template('index.html', results=selected_palette, p_mode=palettes, imagepath=legopath)


if __name__ == '__main__':
    app.run(debug=True)
