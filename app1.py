import string
from urllib.parse import urlparse


app = Flask(__name__)
CORS(app)

@@ -21,7 +20,6 @@ def generate_short_code(length=6):
def home():
return render_template('index.html')


def is_valid_url(url):
try:
if ' ' in url:
@@ -40,17 +38,18 @@ def create_short_url():
data = request.json
original_url = data.get('url')
if not original_url:
        return jsonify({"error": "URL is required"}), 400
        return jsonify({"success": False, "error": "URL is required"}), 400

# Check for valid URL
if not is_valid_url(original_url):
        return jsonify({"error": "URL is invalid"}), 400
        return jsonify({"success": False, "error": "URL is invalid"}), 400

# Check if URL already exists
existing = db.urls.find_one({"url": original_url})
if existing:
existing["id"] = str(existing["_id"])
return jsonify({
            "success": True,
"message": "This URL has already been shortened.",
"data": existing
}), 200
@@ -71,29 +70,28 @@ def create_short_url():
inserted = db.urls.insert_one(url_data)
url_data["id"] = str(inserted.inserted_id)

    return jsonify(url_data), 201

    return jsonify({"success": True, "data": url_data}), 201

@app.route('/shorten/<short_code>', methods=['GET'])
def retrieve_url(short_code):
url = db.urls.find_one({"shortCode": short_code})
if not url:
        return jsonify({"error": "Short URL not found"}), 404
        return jsonify({"success": False, "error": "Short URL not found"}), 404

db.urls.update_one({"shortCode": short_code}, {"$inc": {"accessCount": 1}})
url['id'] = str(url['_id'])
    return jsonify(url)
    return jsonify({"success": True, "data": url})

@app.route('/shorten/<short_code>', methods=['PUT'])
def update_url(short_code):
data = request.json
new_url = data.get("url")
if not new_url:
        return jsonify({"error": "URL is required"}), 400
        return jsonify({"success": False, "error": "URL is required"}), 400

url = db.urls.find_one({"shortCode": short_code})
if not url:
        return jsonify({"error": "Short URL not found"}), 404
        return jsonify({"success": False, "error": "Short URL not found"}), 404

db.urls.update_one(
{"shortCode": short_code},
@@ -102,24 +100,25 @@ def update_url(short_code):

updated = db.urls.find_one({"shortCode": short_code})
updated["id"] = str(updated["_id"])
    return jsonify(updated)
    return jsonify({"success": True, "data": updated})

@app.route('/shorten/<short_code>', methods=['DELETE'])
def delete_url(short_code):
result = db.urls.delete_one({"shortCode": short_code})
if result.deleted_count == 0:
        return jsonify({"error": "Short URL not found"}), 404
    return '', 204
        return jsonify({"success": False, "error": "Short URL not found"}), 404
    return jsonify({"success": True, "message": "Short URL deleted"}), 204

@app.route('/shorten/<short_code>/stats', methods=['GET'])
def get_stats(short_code):
url = db.urls.find_one({"shortCode": short_code})
if not url:
        return jsonify({"error": "Short URL not found"}), 404
        return jsonify({"success": False, "error": "Short URL not found"}), 404

url["id"] = str(url["_id"])
    return jsonify(url)
    return jsonify({"success": True, "data": url})

# Redirect route for short URL
@app.route('/r/<short_code>')
def redirect_short_url(short_code):
url = db.urls.find_one({"shortCode": short_code})
