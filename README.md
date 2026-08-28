#  Passport Photo Pro

A web-based tool to generate print-ready passport photo sheets from uploaded images. Supports multiple photos, per-photo copy counts, AI background removal, image enhancement, and multi-page PDF export — all on an A4 layout at 300 DPI.

## 🧰 Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| Frontend  | HTML, Tailwind CSS, Vanilla JS    |
| Backend   | Python, Flask                     |
| Image AI  | remove.bg API                     |
| PDF gen   | Pillow (PIL)                      |

---

##  Prerequisites

- Python 3.8+
- pip
- A [remove.bg](https://www.remove.bg/api) API key

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

>  Never commit your `.env` file. Add it to `.gitignore`.

### 4. Run the app

```bash
python app.py
```

The server will start at `http://localhost:5000`.

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


---

## 📄 License

MIT License. See `LICENSE` for details.
