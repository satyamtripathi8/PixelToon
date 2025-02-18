from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import os
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads/"
PROCESSED_FOLDER = "static/processed/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def apply_cartoon_effect(image, effect_type):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    smooth = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(smooth, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(image, 9, 300, 300)
    
    if effect_type == "cartoon":
        return cv2.bitwise_and(color, color, mask=edges)
    elif effect_type == "pencil_gray":
        return cv2.cvtColor(cv2.bitwise_not(edges), cv2.COLOR_GRAY2BGR)
    elif effect_type == "pencil_color":
        return cv2.bitwise_and(color, cv2.bitwise_not(edges))
    elif effect_type == "oil_painting":
        return cv2.xphoto.oilPainting(image, 7, 1)
    elif effect_type == "watercolor":
        return cv2.stylization(image, sigma_s=60, sigma_r=0.6)
    return image

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cartoonify', methods=['POST'])
def cartoonify():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    effect = request.form.get('effect', 'cartoon')
    
    try:
        image = Image.open(file.stream)
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        processed_image = apply_cartoon_effect(image, effect)
        processed_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
        
        _, buffer = cv2.imencode('.png', processed_image)
        encoded_image = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({"processed_image": f"data:image/png;base64,{encoded_image}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)