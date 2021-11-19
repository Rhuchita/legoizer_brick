from flask import Flask, render_template, flash, request, redirect, url_for
import legofy
from PIL import Image
import webcolors
from colorthief import ColorThief
import os
port = int(os.environ.get('PORT',5000))

app = Flask(__name__)


def color_palette(image_path):
    image_colors = []
    with open(image_path, 'r+b') as f:
        with Image.open(f) as image:
            color_thief = ColorThief(image_path)
            color_palette = color_thief.get_palette(
                color_count=10, quality=10)
            for color in color_palette:
                image_colors.append(webcolors.rgb_to_hex(color))
    return image_colors


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
        img_path = "static/"+legopath

        selected_palette = color_palette(img_path)
        return render_template('index.html', results=selected_palette, p_mode=palettes, imagepath=legopath)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
