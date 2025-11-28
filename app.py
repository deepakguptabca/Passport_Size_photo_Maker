from flask import Flask, request, render_template, send_file
from PIL import Image, ImageOps
from io import BytesIO
from dotenv import load_dotenv
import requests
import cloudinary
import cloudinary.uploader
import cloudinary.utils
import os
import base64

app = Flask(__name__)

# Cloudinary + Remove.bg API setup
REMOVE_BG_API_KEY = os.getenv("REMOVE_BG_API_KEY")

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    print("==== /process endpoint hit ====")

    if "image" not in request.files:
        print("DEBUG: No image in request")
        return "No image uploaded", 400

    file = request.files["image"]
    print(f"DEBUG: Received image file: {file.filename}")
    input_image = file.read()

    # Layout settings
    passport_width = 384
    passport_height = 472
    border = 2
    spacing = 25
    margin_x = 10
    margin_y = 15
    horizontal_gap = 20
    a4_w, a4_h = 2480, 3508
    copies = int(request.form.get("copies", 6))
    print(f"DEBUG: Copies requested = {copies}")

    # Step 1: Background removal
    print("DEBUG: Sending image to remove.bg...")
    response = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": input_image},
        data={"size": "auto"},
        headers={"X-Api-Key": REMOVE_BG_API_KEY},
    )
    print(f"DEBUG: remove.bg response status = {response.status_code}")

    if response.status_code != 200:
        print(f"ERROR: Background removal failed - {response.text}")
        try:
            error_info = response.json()
            if error_info.get("errors"):
                error_code = error_info["errors"][0].get("code", "unknown_error")
                return {"error": error_code}, 410
        except Exception as ex:
            print("Failed to parse error:", ex)

        return {"error": "bg_removal_failed"}, 500

    bg_removed = BytesIO(response.content)
    img = Image.open(bg_removed)
    print(f"DEBUG: Image mode after background removal: {img.mode}")

    if img.mode in ("RGBA", "LA"):
        print("DEBUG: Converting transparent background to white")
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1])
        processed_img = background
    else:
        processed_img = img.convert("RGB")

    # Step 2: Upload cleaned image to Cloudinary
    buffer = BytesIO()
    processed_img.save(buffer, format="PNG")
    buffer.seek(0)
    print("DEBUG: Uploading to Cloudinary...")

    upload_result = cloudinary.uploader.upload(buffer, resource_type="image")
    image_url = upload_result.get("secure_url")
    public_id = upload_result.get("public_id")

    print(f"DEBUG: Cloudinary URL: {image_url}")

    if not image_url:
        print("ERROR: Failed to get image URL from Cloudinary.")
        return "Cloudinary upload failed", 500

    # Step 3: Enhance image via Cloudinary AI
    print("DEBUG: Enhancing image via Cloudinary...")

    enhanced_url = cloudinary.utils.cloudinary_url(
        public_id,
        transformation=[
            {"effect": "gen_restore"},  # AI image enhancement
            {"quality": "auto"},  # auto optimize
            {"fetch_format": "auto"},  # auto format (webp)
        ],
    )[0]

    print(f"DEBUG: Enhanced image URL = {enhanced_url}")

    # Download enhanced image
    enhanced_img_data = requests.get(enhanced_url).content
    img = Image.open(BytesIO(enhanced_img_data))
    print("DEBUG: Enhanced image downloaded")

    # Step 4: Convert back to RGB (if needed)
    if img.mode in ("RGBA", "LA"):
        print("DEBUG: Removing transparency after enhancement")
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1])
        passport_img = background
    else:
        passport_img = img.convert("RGB")

    # Step 5: Resize + border
    passport_img = passport_img.resize((passport_width, passport_height), Image.LANCZOS)
    passport_img = ImageOps.expand(passport_img, border=border, fill="black")
    print(f"DEBUG: Passport image size after border = {passport_img.size}")

    # Step 6: Fill A4 layout
    a4 = Image.new("RGB", (a4_w, a4_h), "white")
    x, y = margin_x, margin_y
    paste_w = passport_width + 2 * border
    paste_h = passport_height + 2 * border
    placed = 0

    print("DEBUG: Placing images on A4...")

    for _ in range(copies):
        if x + paste_w > a4_w:
            x = margin_x
            y += paste_h + spacing

        if y + paste_h > a4_h:
            print("DEBUG: Reached end of page")
            break

        a4.paste(passport_img, (x, y))
        print(f"DEBUG: Placed copy {placed + 1} at x={x}, y={y}")
        x += paste_w + horizontal_gap
        placed += 1

    print(f"DEBUG: Total placed = {placed}")

    # Step 7: Export PDF
    output = BytesIO()
    a4.save(output, format="PDF", dpi=(300, 300))
    output.seek(0)
    print("DEBUG: Returning PDF to client")

    return send_file(
        output,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="passport-sheet.pdf",
    )


if __name__ == "__main__":
    app.run(debug=True)
