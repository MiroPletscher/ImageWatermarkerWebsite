from flask import Flask, request, jsonify, render_template
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import base64

app = Flask(__name__)
app.secret_key = "7d5c2a2d6136fbf166211d5183bf66214a247f31"

def add_watermark_with_opacity(base_img, watermark_img, opacity):
    # Resize watermark to fit on the base image
    watermark_width, watermark_height = watermark_img.size
    base_width, base_height = base_img.size
    ratio = min(base_width / watermark_width, base_height / watermark_height)
    new_width = int(watermark_width * ratio)
    new_height = int(watermark_height * ratio)
    resized_watermark = watermark_img.resize((new_width, new_height), Image.ANTIALIAS)

    # Calculate position to place watermark in the center
    position = ((base_width - new_width) // 2, (base_height - new_height) // 2)

    # Create a transparent overlay with the same size as the base image and convert it to the mode of the base image
    overlay = Image.new('RGBA', base_img.size, (0, 0, 0, 0)).convert(base_img.mode)

    # Paste the resized watermark onto the overlay
    overlay.paste(resized_watermark, position)

    # Blend the overlay with the base image using the specified opacity
    watermarked_img = Image.blend(base_img, overlay, opacity)

    return watermarked_img

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'images' not in request.files or 'watermark_image' not in request.files:
            return jsonify({'error': 'Please provide both images and watermark'}), 400

        images = request.files.getlist('images')
        watermark = request.files['watermark_image']

        opacity = float(request.form.get('opacity', 0.5))  # Default opacity is 0.5 if not specified
        scale = float(request.form.get('scale', 1.0))  # Default scale is 1.0 if not specified

        watermarked_images = []

        for image in images:
            img = Image.open(image)
            watermark_img = Image.open(watermark)

            # Resize watermark image based on scale
            watermark_width, watermark_height = watermark_img.size
            new_width = int(watermark_width * scale)
            new_height = int(watermark_height * scale)
            resized_watermark = watermark_img.resize((new_width, new_height), Image.ANTIALIAS)

            watermarked_img = add_watermark_with_opacity(img, resized_watermark, opacity)

            # Convert the watermarked image to bytes
            buffered = BytesIO()
            watermarked_img.save(buffered, format='JPEG')

            # Encode the bytes object to base64 string
            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

            watermarked_images.append(img_base64)

        return jsonify({'watermarked_images': watermarked_images}), 200
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)