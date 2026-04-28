from flask import Flask, render_template, request, url_for
import os
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create folder if not exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/", methods=["GET", "POST"])
def index():
    output_text = ""

    if request.method == "POST":

        # Save uploaded letters
        for letter in "abcdefghijklmnopqrstuvwxyz":
            file = request.files.get(letter)

            if file and file.filename != "":
                path = os.path.join(app.config["UPLOAD_FOLDER"], f"{letter}.png")

                # Resize image to consistent size
                img = Image.open(file)
                img = img.convert("RGBA")
                img = img.resize((40, 40))
                img.save(path)

        # Get user text
        text = request.form.get("text", "").lower()

        # Generate handwritten output
        for char in text:
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], f"{char}.png")

            if os.path.exists(file_path):
                img_url = url_for("static", filename=f"uploads/{char}.png")
                output_text += f'<img src="{img_url}" class="letter">'
            elif char == " ":
                output_text += "&nbsp;&nbsp;"
            elif char == "\n":
                output_text += "<br>"
            else:
                output_text += char  # fallback for punctuation

    return render_template("index.html", output_text=output_text)


if __name__ == "__main__":
    app.run(debug=True)
