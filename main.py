#pip install flask opencv-python

from flask import Flask  
from flask import render_template
from flask import request
from flask import flash
from flask import Flask
from flask import flash
from flask import request
from werkzeug.utils import secure_filename
import cv2
import os



UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','webp'}




app = Flask(__name__)
app.secret_key = 'super secret key'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, operation):
#def processImage():
    print(f"the operation is {operation} and filename is {filename}")
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFilename = f"static/{filename}"
            cv2.imwrite(f"static/{filename}", imgProcessed)
            return newFilename
        case "cwebp":
            newFilename = f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cjpg":
            newFilename = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cpng":
            newFilename = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newFilename, img)
            return newFilename
    pass
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/About")
def About():
    return render_template("About.html")

@app.route("/edit", methods = ["GET", "POST"])
def edit():
    if request.method == "POST":
        operation = request.form.get("operation")
         # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "error no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename) # type: ignore
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, operation)
            flash(f"Your image has been processed and is available <a href='/{new}' target='_blank'>here</a>")
            #processImage()
            print (f"the operation is {operation} and filename is {filename}")
            return render_template("index.html")
           
           
           
    #return redirect(url_for('download_file', name=filename))
    
#return "POST request is here"
    return render_template("index.html")

#@app.route("/How_To_Use")
#def HowToUse():
#    return render_template("How_To_Use.html")

#To run the server 
app.run(debug= True)