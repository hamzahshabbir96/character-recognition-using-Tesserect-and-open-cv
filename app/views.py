from app import app
from flask import request, render_template, url_for
import os
import cv2
import numpy as np
from PIL import Image
import random
import string
import pytesseract
#download tesserect
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Adding path to config
app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'
language='eng'
@app.route("/", methods=["GET", "POST"])
def index():

	# Execute if request is get
	if request.method == "GET":
		file_name =  'images/default.jpg'
		return render_template("index1.html", full_filename = full_filename)

	# Execute if reuqest is post
	if request.method == "POST":


		id_image = request.files['image_upload']
		imagename = id_image.filename
		image = Image.open(image_upload)

		# Converting image to array
		image_arr = np.array(image.convert('RGB'))
		# Converting image to grayscale
		gray_img_arr = cv2.cvtColor(image_arr, cv2.COLOR_BGR2GRAY)
		#Converting image back to rbg
		image = Image.fromarray(gray_img_arr)

		# Printing lowercase
		letters = string.ascii_lowercase
		# Generating unique image name for dynamic image display
		name = ''.join(random.choice(letters) for i in range(10)) + '.png'
		file_name =  'uploads/' + name

		# Extracting text from image
		custom_config = '-l '+language+' --oem 3 --psm 6'
		text = pytesseract.image_to_string(image,config=custom_config)

		# Remove symbol if any
		characters_to_remove = "!()@—*“>+-/,'|£#%$&^_~"
		new_string = text
		for character in characters_to_remove:
			new_string = new_string.replace(character, "")

		# Converting string into list to dislay extracted text in seperate line
		new_string = new_string.split("\n")

		# Saving image to display in html
		img = Image.fromarray(image_arr, 'RGB')
		img.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], name))
		# Returning template, filename, extracted text
		return render_template('index1.html', file_name = file_name, text = new_string)


@app.route('/about/', methods=["GET"])
def about():
	if request.method == "GET":

		return render_template('About.html')

# Main function
if __name__ == '__main__':
    app.run(debug=True)
