# 📸 Passport Photo Pro

A web-based tool to generate print-ready passport photo sheets from uploaded images. Supports multiple photos, per-photo copy counts, AI background removal, image enhancement, and multi-page PDF export — all on an A4 layout at 300 DPI.
---
### Silent Contributor 
  Base code - [Abacusus](https://github.com/abacusus)
  
---

## 🚀 Features

- **Multi-photo upload** — drag & drop or click to upload one or more photos at once
- **Per-photo copy count** — set how many copies of each photo you need (1–54)
- **In-browser cropper** — crop each photo to the correct passport aspect ratio before processing
- **AI background removal** — powered by [remove.bg](https://www.remove.bg/)
- **AI image enhancement** — restored and sharpened via [Cloudinary's gen_restore](https://cloudinary.com/documentation/image_transformations)
- **A4 print layout** — photos are automatically arranged in a grid at 300 DPI
- **Multi-page PDF** — if photos exceed one A4 page, additional pages are created automatically
- **Advanced options** — customize photo width, height, spacing, and border size
- **Feedback system** — built-in bug report form powered by EmailJS
- **Animated particle background** — via Particles.js

---

## 🧰 Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| Frontend  | HTML, Tailwind CSS, Vanilla JS    |
| Cropping  | Cropper.js                        |
| Backend   | Python, Flask                     |
| Image AI  | remove.bg API, Cloudinary AI      |
| PDF gen   | Pillow (PIL)                      |
| Email     | EmailJS                           |

---

## 📦 Prerequisites

- Python 3.8+
- pip
- A [remove.bg](https://www.remove.bg/api) API key
- A [Cloudinary](https://cloudinary.com/) account (free tier works)

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/passport-photo-pro.git
cd passport-photo-pro
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ Never commit your `.env` file. Add it to `.gitignore`.

### 4. Run the app

```bash
python app.py
```

The server will start at `http://localhost:5000`.

---

## 📁 Project Structure

```
passport-photo-pro/
├── app.py                  # Flask backend — image processing & PDF generation
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not committed)
├── templates/
│   └── index.html          # Frontend UI
└── README.md
```

---

## 📋 requirements.txt

Make sure your `requirements.txt` includes:

```
flask
pillow
requests
python-dotenv
cloudinary
```

Generate it automatically with:

```bash
pip freeze > requirements.txt
```

---

## 🖼️ How It Works

### Upload
- Open the app in your browser at `http://localhost:5000`
- Drag and drop one or more photos onto the upload zone, or click to browse
- Each photo appears as a card with a thumbnail

### Crop (Optional but Recommended)
- Click **Crop** on any photo card
- A modal cropper opens with a fixed passport aspect ratio (384×472)
- Adjust the crop area and click **Crop & Save**

### Set Copies
- Each photo card has a **Copies** input (default: 6)
- Change it per photo to control how many times it appears on the sheet

### Advanced Options (Optional)
- Click **Advanced Options** to customize:
  - **Width / Height** — passport photo dimensions in pixels
  - **Spacing** — gap between rows of photos
  - **Border** — black border thickness around each photo

### Generate
- Click **Generate Sheet**
- The backend processes each photo:
  1. Removes the background via remove.bg
  2. Uploads to Cloudinary and applies AI restoration
  3. Resizes and adds a border
- All photos are arranged on A4 pages (2480×3508 px at 300 DPI)
- If photos overflow one page, new pages are added automatically

### Download
- Once generated, a PDF preview appears in the browser
- Click **Download PDF** to save the print-ready file

---

## ⚙️ API Endpoints

| Method | Route      | Description                          |
|--------|------------|--------------------------------------|
| GET    | `/`        | Serves the frontend UI               |
| POST   | `/process` | Accepts images, returns a PDF stream |

### `/process` Form Data

| Field       | Type    | Description                              |
|-------------|---------|------------------------------------------|
| `image_0`   | File    | First uploaded image                     |
| `copies_0`  | Integer | Number of copies for image 0             |
| `image_1`   | File    | Second uploaded image (if any)           |
| `copies_1`  | Integer | Number of copies for image 1             |
| `width`     | Integer | Passport photo width in px (default 400) |
| `height`    | Integer | Passport photo height in px (default 400)|
| `spacing`   | Integer | Row spacing in px (default 25)           |
| `border`    | Integer | Border size in px (default 2)            |

---

## 🔐 Environment Variables Reference

| Variable                | Description                          |
|-------------------------|--------------------------------------|
| `REMOVE_BG_API_KEY`     | API key from remove.bg               |
| `CLOUDINARY_CLOUD_NAME` | Your Cloudinary cloud name           |
| `CLOUDINARY_API_KEY`    | Cloudinary API key                   |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret                |

---

## 🐛 Known Limitations

- remove.bg has a daily free-tier quota — heavy usage may return a `429` error
- Very large images may slow down processing
- The Cloudinary `gen_restore` transformation may not be available on all plans

---

## 📬 Feedback & Bug Reports

Use the red chat button in the bottom-right corner of the app to submit feedback or report bugs directly from the UI.

---

## 📄 License

MIT License. See `LICENSE` for details.
