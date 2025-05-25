# Tooba-Innovaxel-Eman
1.
   # 🔗 Innovaxel URL Shortener
   #  Innovaxel URL Shortener

A simple Flask-based URL shortening service built with MongoDB.  
This app allows users to create, update, rretrive, delete, and view statistics of shortened URLs with a web UI.

---

## 🚀 Features
##  Features

- Shorten any URL into a custom code
- Track number of times the short URL was accessed
@@ -16,7 +16,7 @@

---

## 🛠️ Tech Stack
##  Tech Stack

- *Backend:* Flask (Python)
- *Database:* MongoDB
@@ -25,47 +25,47 @@

---

## ⚙️ Setup Instructions
##  Setup Instructions

~bash
1. *Clone the repo:*
```bash
git clone https://github.com/Tooba-Eman/Tooba-Innovaxel-Eman.git
cd Tooba-Innovaxel-Eman
git checkout dev

~bash
2. *Create Virtual Environment*
python -m venv venv
source venv/bin/activate

~bash 
4. *Install dependencies*
pip install -r requirements.txt


5. Start MongoDB (ensure it’s running on mongodb://localhost:27017)

~bash
6. *Run the app*
python app1.py


7. *Open in browser*
http://localhost:5000 





*Project Structure*
Tooba-Innovaxel-Eman/
│
├── app1.py               # Flask backend
├── templates/
│   └── index.html       # UI frontend
├── static/
│   └── style.css        # css for attractive visualization
├── requirements.txt     # Python packages
└── README.md            # Project info
