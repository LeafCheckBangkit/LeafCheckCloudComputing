from flask import Flask, render_template, request, redirect, url_for, flash
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
import os

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necessary for flash messages
model = load_model('./Pred_model_FIX0.96.h5')  # Load the pre-trained model

# Set the upload folder and allowed file extensions
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

@app.route('/')
def index_view():
    # Render the index page
    return render_template('index.html')

def allowed_file(filename):
    # Check if the uploaded file has one of the allowed extensions
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(file_path, target_size=(224, 224)):
    # Load, resize, convert to array, and preprocess the image
    img = load_img(file_path, target_size=target_size)
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            try:
                # Process the image
                img = load_img(file_path, target_size=(150, 150))
                x = img_to_array(img)
                x /= 255.0
                x = np.expand_dims(x, axis=0)
                images = np.vstack([x])

                # Make the prediction
                classes = model.predict(images, batch_size=10)
                print(classes[0])
                predicted_class = np.argmax(classes[0])

                # Map the predicted class to the label
                if predicted_class == 0:
                    label = "healthy apple leaves"
                    notes = "SEHAT BANGET NIH POHONNYA INGPO BAGI BAGI"
                elif predicted_class == 1:
                    label = "unhealthy apple leaves"
                    notes = "TEBANG AJA DAH"
                elif predicted_class == 2:
                    label = "healthy mango leaves"
                    notes = "INGPO NGERUJAK"
                elif predicted_class == 3:
                    label = "unhealthy mango leaves"
                    notes = "BAKARRRRR"
                elif predicted_class == 4:
                    label = "healthy orange leaves"
                    notes = "JUALAN JUS JERUK LAKU NIH"
                elif predicted_class == 5:
                    label = "unhealthy orange leaves"
                    notes = "TAMBAHIN PUPUK BANG"

                return render_template('predict.html', leaf=label, prob=classes[0], user_image=filename, keterangan=notes)
            except Exception as e:
                flash(f"Error processing image: {str(e)}")
                return redirect(request.url)
        else:
            flash('Unsupported file extension')
            return redirect(request.url)
    
    return render_template('index.html')

# Run the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=False, port='8080')