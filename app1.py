import string
from urllib.parse import urlparse


app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/urlShortener"
mongo = PyMongo(app)
db = mongo.db


def generate_short_code(length=6):
return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@@ -33,6 +33,7 @@ def is_valid_url(url):
return True
except Exception:
return False
    

@app.route('/shorten', methods=['POST'])
def create_short_url():
@@ -49,6 +50,7 @@ def create_short_url():
existing = db.urls.find_one({"url": original_url})
if existing:
existing["id"] = str(existing["_id"])
        existing["short_url"] = request.host_url.rstrip('/') + '/r/' + existing["shortCode"]
return jsonify({
"success": True,
"message": "This URL has already been shortened.",
@@ -71,8 +73,12 @@ def create_short_url():
inserted = db.urls.insert_one(url_data)
url_data["id"] = str(inserted.inserted_id)

    url_data["short_url"] = request.host_url.rstrip('/') + '/r/' + short_code

return jsonify({"success": True, "data": url_data}), 201



@app.route('/shorten/<short_code>', methods=['GET'])
def retrieve_url(short_code):
url = db.urls.find_one({"shortCode": short_code})eturn ''.join(random.choices(string.ascii_letters + string.digits, k=length))
