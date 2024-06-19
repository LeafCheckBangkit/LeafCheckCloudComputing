from flask import Flask, render_template, request, redirect, url_for, flash
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
import os

# Initialize the Flask application
app = Flask(__name__)
model = load_model('./model.h5')  # Load the pre-trained model
app.secret_key = 'supersecretkey'  # Necessary for flash messages
# Set the upload folder and allowed file extensions
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
    
@app.route('/')
def index_view():
    # Render the index page
    return {"msg":"API READY"}

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
            return {"error":"no file part"}
        
        file = request.files['file']
        
        if file.filename == '':
            return{"error":"File masih kososng"}
        
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
                    notes = "Daun buah apel yang sehat berwarna hijau cerah, mengilap, dan bebas dari bintik-bintik atau lubang. Bentuk daun biasanya oval dengan tepi bergerigi dan urat-urat daun terlihat jelas. Daun terasa kuat dan elastis saat disentuh."
                    tips1 = "Perhatikan warna daun, daun yang hijau cerah menandakan kondisi yang sehat."
                    tips2 = "Pastikan daun bebas dari serangga atau tanda-tanda penyakit."
                    tips3 = "Lakukan penyiraman dan pemupukan secara rutin untuk menjaga kesehatan daun."
                    trick1 = "Semprotkan campuran air dan sabun ringan untuk menghilangkan serangga yang menempel pada daun."
                    trick2 = "Pangkas daun yang rusak atau terinfeksi untuk mencegah penyebaran penyakit." 
                elif predicted_class == 1:
                    label = "unhealthy apple leaves"
                    notes = "Daun buah apel yang tidak sehat sering kali berwarna kuning, cokelat, atau memiliki bintik-bintik hitam. Daun bisa tampak layu, kusam, dan mungkin memiliki lubang akibat serangan hama atau penyakit. Tekstur daun biasanya kering atau rapuh"
                    tips1 = "Periksa daun secara rutin untuk tanda-tanda penyakit atau hama."
                    tips2 = "Segera tangani daun yang terkena penyakit dengan fungsida atau insektisida sesuai kebutuhan."
                    tips3 = "Jaga kebersihan area sekitar pohon untuk mengurangi risiko infeksi."
                    trick1 = "Gunakan campuran air dan baking soda untuk mengatasi jamur pada daun."
                    trick2 = "Komposkan daun yang telah gugur dan terkena penyakit jauh dari tanaman untuk mencegah penyebaran." 
                elif predicted_class == 2:
                    label = "healthy mango leaves"
                    notes = "Daun mangga yang sehat memiliki warna hijau tua dan mengilap, dengan urat daun yang terlihat jelas. Bentuknya lonjong dan ujung meruncing, dengan permukaan yang halus dan tekstur yang kuat serta elastis."
                    tips1 =  "Pastikan pohon mangga mendapatkan cukup sinar matahari dan air"
                    tips2 = "Periksa daun secara rutin untuk mendeteksi tanda-tanda penyakit atau hama lebih awal."
                    tips3 = "Berikan pupuk yang kaya akan nitrogen untuk mendukung pertumbuhan daun yang sehat."
                    trick1 = "Semprotkan campuran air dan sabun untuk mengusir serangga yang menempel."
                    trick2 = "Gunakan mulsa organik untuk menjaga kelembaban tanah dan kesehatan akar." 
                elif predicted_class == 3:
                    label = "unhealthy mango leaves"
                    notes = "Daun mangga yang tidak sehat sering kali berwarna kuning, cokelat, atau terdapat bintik-bintik hitam. Daun mungkin terlihat keriput, layu, atau berlubang akibat hama. Tekstur daun biasanya kering dan mudah patah."
                    tips1 = "Periksa daun secara rutin untuk mendeteksi masalah sejak dini"
                    tips2 = "Gunakan fungisida atau insektisida alami untuk mengatasi masalah pada daun."
                    tips3 = "Jaga kebersihan area sekitar pohon untuk mencegah penyebaran penyakit."
                    trick1 = "Pangkas daun yang terinfeksi untuk mencegah penyebaran penyakit."
                    trick2 = "Komposkan daun yang sehat untuk memperkaya tanah dengan nutrisi tambahan." 
                elif predicted_class == 4:
                    label = "healthy orange leaves"
                    notes = "Daun jeruk yang sehat berwarna hijau tua, mengilap, dan memiliki tekstur yang halus. Daun berbentuk oval atau lonjong dengan ujung meruncing dan urat-urat daun terlihat jelas. Daun terasa kenyal saat disentuh dan bebas dari bintik atau kerusakan"
                    tips1 = "Jaga kelembaban tanah dan pastikan pohon jeruk mendapatkan sinar matahari yang cukup."
                    tips2 = "Periksa daun secara rutin untuk memastikan tidak ada tanda-tanda penyakit atau hama."
                    tips3 = "Berikan pupuk secara teratur untuk memastikan nutrisi yang cukup bagi tanaman."
                    trick1 = "Gunakan mulsa di sekitar pohon untuk menjaga kelembaban tanah."
                    trick2 = "Semprotkan campuran minyak neem untuk mencegah serangan serangga pada daun." 
                elif predicted_class == 5:
                    label = "unhealthy orange leaves"
                    notes = "Daun jeruk yang tidak sehat biasanya berwarna kuning, cokelat, atau memiliki bercak-bercak hitam. Daun dapat terlihat layu, keriput, atau berlubang akibat hama. Tekstur daun kering dan rapuh"
                    tips1 = "Periksa daun secara rutin dan segera tangani jika ditemukan tanda-tanda penyakit atau hama."
                    tips2 = "Gunakan insektisida alami seperti minyak neem untuk mengatasi serangga."
                    tips3 = "Jaga kebersihan area sekitar pohon untuk mengurangi risiko infeksi."
                    trick1 = "Pangkas daun yang terkena penyakit untuk mencegah penyebaran lebih lanjut."
                    trick2 = "Gunakan kompos dari daun sehat untuk memberikan nutrisi tambahan pada tanaman." 

                return {
                    "leaf":label, 
                    "user_image":filename, 
                    "keterangan":notes, 
                    "tips1":tips1, 
                    "tips2":tips1, 
                    "tips3":tips1, 
                    "trick1":trick1, 
                    "trick2":trick2
                    }
            except Exception as e:
                return{"error":"error processing image"}
        else:
            return {"error":"Ekstensi file tidak di dukung"}
    return{
        "cond" : "API SIAP DIPAKAI"
    }

# Run the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=False, port='8080')