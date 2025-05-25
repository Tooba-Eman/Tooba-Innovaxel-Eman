from datetime import datetime
import random
import string
from urllib.parse import urlparse


app = Flask(__name__)
CORS(app)
@@ -19,15 +21,32 @@ def generate_short_code(length=6):
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
return jsonify({"error": "URL is required"}), 400

    # Check for valid URL
    if not is_valid_url(original_url):
        return jsonify({"error": "URL is invalid"}), 400

       # Check if URL already exists
    # Check if URL already exists
existing = db.urls.find_one({"url": original_url})
if existing:
existing["id"] = str(existing["_id"])
@@ -53,6 +72,40 @@ def create_short_url():
url_data["id"] = str(inserted.inserted_id)

return jsonify(url_data), 201


@app.route('/shorten/<short_code>', methods=['GET'])
