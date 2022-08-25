from flask import Flask, render_template, request, session
import pandas as pd
from PIL import Image, ImageOps
import requests
from io import BytesIO
import numpy as np
import os
import uuid


app = Flask(__name__)
app.config['SECRET_KEY'] = "K:JDLKFJMSLKVNKIp"

hotel_ids = pd.read_csv("hotel_ids.csv")
objects = pd.read_csv("img_objects.csv")


def save_patches(hotel_id, object_category):

    for f in os.listdir("./static/images/gallery"):
        os.remove(os.path.join("./static/images/gallery", f))
    for f in os.listdir("./static/images/test"):
        os.remove(os.path.join("./static/images/test", f))
    
    mask = (objects["hotel_id"] == hotel_id) & (objects["object_category"] == object_category)
    object_df = objects.loc[mask]

    gallery_patches = []
    test_patches = []

    for _, object in object_df.iterrows():
        response = requests.get(object["image_url"])
        img = Image.open(BytesIO(response.content)).convert("RGB")
        img = ImageOps.exif_transpose(img)
        img = img.resize((224,224))

        bbox = object["object_bbox"]
        bbox = bbox.replace("[","").replace("]","").split(",")
        bbox = [int(x) for x in bbox]

        patch = np.array(img)
        patch = patch[bbox[0]:bbox[2],bbox[1]:bbox[3],:]
        patch = Image.fromarray(patch)

        if object["dataset"] == "gallery":
            path = f"static/images/gallery/{object['image_id']}-{object_category}.png"
            gallery_patches.append(path)
            patch.save(path)
        else:
            path = f"static/images/test/{object['image_id']}-{object_category}.png"
            test_patches.append(path)
            patch.save(path)

    return gallery_patches, test_patches


def get_hotel_at_index(index):
    row = hotel_ids.iloc[index]
    return row["hotel_id"], row["object_category"]


@app.route("/", methods=["GET", "POST"])
def index():

    if "index" not in session:
        session["index"] = 0

    if request.method == "POST":
        form_name = request.form.get("form_name")

        if form_name == "custom_index_form":
            custom_index = int(request.form['custom_index'])
            session["index"] = custom_index

        elif form_name == "next_form":
            session["index"] = session["index"] + 1

        elif form_name == "previous_form":
            session["index"] = session["index"] - 1

    hotel_id, category = get_hotel_at_index(session["index"])

    gallery_patches, test_patches = save_patches(hotel_id, category)

    data = {'unique_combos': len(hotel_ids.index),
            'current_index': session["index"],
            'hotel_id': hotel_id, 
            'object_category': category,
            'gallery_patches': gallery_patches,
            'gallery_patches_len': len(gallery_patches),
            'test_patches': test_patches,
            'test_patches_len': len(test_patches)}

    return render_template("index.html", data=data)


if __name__ == "__main__": 
    app.run(host='0.0.0.0')

