import os
from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
from gemini import GeminiClient

app = Flask(__name__, template_folder="templates")

app.config["SECRET_KEY"] = "secert_key"
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

class UploadFileForm(FlaskForm):
    file = FileField("Audio file", validators=[DataRequired()])
    submit = SubmitField("Upload Audio")


@app.route("/", methods=["GET", "POST"])
def home():
    form = UploadFileForm()
    gemini_output = None  # default empty

    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)

        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(save_path)

        client = GeminiClient(model_name="gemini-2.5-flash")
        gemini_output = client.build_response(file_name=save_path)

        flash("File processed successfully!", "success")

        return render_template("index.html", form=form, output=gemini_output)

    return render_template("index.html", form=form, output=gemini_output)


if __name__ == "__main__":
    app.run(debug=True)
