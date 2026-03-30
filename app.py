from flask import Flask, render_template, request
import os
from PIL import Image

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Store uploaded letter images
letter_images = {}

@app.route("/", methods=["GET", "POST"])
def index():
    output_text = ""

    if request.method == "POST":
        # Upload letters
        for letter in "abcdefghijklmnopqrstuvwxyz":
            file = request.files.get(letter)
            if file:
                path = os.path.join(app.config["UPLOAD_FOLDER"], f"{letter}.png")
                file.save(path)
                letter_images[letter] = path

        # Generate handwritten text
        text = request.form.get("text").lower()
        output_text = ""

        for char in text:
            if char in letter_images:
                output_text += f'<img src="/{letter_images[char]}" width="30">'
            elif char == " ":
                output_text += " "
    
    return render_template("index.html", output_text=output_text)


if __name__ == "__main__":
    app.run(debug=True)