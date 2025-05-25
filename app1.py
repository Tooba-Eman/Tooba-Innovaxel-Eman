from flask import Flask, request, jsonify, redirect, render_template
from flask_pymongo import PyMongo
from flask_cors import CORS
from datetime import datetime
import random
import string
from urllib.parse import urlparse


app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/urlShortener"
mongo = PyMongo(app)
db = mongo.db

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/')
def home():
    return render_template('index.html')

def is_valid_url(url):
    try:
        if ' ' in url:
            return False

        parsed = urlparse(url)
        if parsed.scheme not in ('http', 'https') or not parsed.netloc:
            return False

        return True
    except Exception:
        return False
    

@app.route('/shorten', methods=['POST'])
def create_short_url():
    data = request.json
    original_url = data.get('url')
    if not original_url:
        return jsonify({"success": False, "error": "URL is required"}), 400

    # Check for valid URL
    if not is_valid_url(original_url):
        return jsonify({"success": False, "error": "URL is invalid"}), 400

    # Check if URL already exists
    existing = db.urls.find_one({"url": original_url})
    if existing:
        existing["id"] = str(existing["_id"])
        existing["short_url"] = request.host_url.rstrip('/') + '/r/' + existing["shortCode"]
        return jsonify({
            "success": True,
            "message": "This URL has already been shortened.",
            "data": existing
        }), 200

    # Generate unique short code
    short_code = generate_short_code()
    while db.urls.find_one({"shortCode": short_code}):
        short_code = generate_short_code()

    now = datetime.utcnow().isoformat()
    url_data = {
        "url": original_url,
        "shortCode": short_code,
        "createdAt": now,
        "updatedAt": now,
        "accessCount": 0
    }
    inserted = db.urls.insert_one(url_data)
    url_data["id"] = str(inserted.inserted_id)

    url_data["short_url"] = request.host_url.rstrip('/') + '/r/' + short_code

    return jsonify({"success": True, "data": url_data}), 201



@app.route('/shorten/<short_code>', methods=['GET'])
def retrieve_url(short_code):
    url = db.urls.find_one({"shortCode": short_code})
    if not url:
        return jsonify({"success": False, "error": "Short URL not found"}), 404

    db.urls.update_one({"shortCode": short_code}, {"$inc": {"accessCount": 1}})
    url['id'] = str(url['_id'])
    return jsonify({"success": True, "data": url})

@app.route('/shorten/<short_code>', methods=['PUT'])
def update_url(short_code):
    data = request.json
    new_url = data.get("url")
    if not new_url:
        return jsonify({"success": False, "error": "URL is required"}), 400

    url = db.urls.find_one({"shortCode": short_code})
    if not url:
        return jsonify({"success": False, "error": "Short URL not found"}), 404

    db.urls.update_one(
        {"shortCode": short_code},
        {"$set": {"url": new_url, "updatedAt": datetime.utcnow().isoformat()}}
    )

    updated = db.urls.find_one({"shortCode": short_code})
    updated["id"] = str(updated["_id"])
    return jsonify({"success": True, "data": updated})

@app.route('/shorten/<short_code>', methods=['DELETE'])
def delete_url(short_code):
    result = db.urls.delete_one({"shortCode": short_code})
    if result.deleted_count == 0:
        return jsonify({"success": False, "error": "Short URL not found"}), 404
    return jsonify({"success": True, "message": "Short URL deleted"}), 204

@app.route('/shorten/<short_code>/stats', methods=['GET'])
def get_stats(short_code):
    url = db.urls.find_one({"shortCode": short_code})
    if not url:
        return jsonify({"success": False, "error": "Short URL not found"}), 404

    url["id"] = str(url["_id"])
    return jsonify({"success": True, "data": url})

# Redirect route for short URL
@app.route('/r/<short_code>')
def redirect_short_url(short_code):
    url = db.urls.find_one({"shortCode": short_code})
    if not url:
        return render_template('404.html'), 404

    db.urls.update_one({"shortCode": short_code}, {"$inc": {"accessCount": 1}})
    return redirect(url['url'])



if __name__ == '__main__':
    app.run(debug=True, port=5000)
