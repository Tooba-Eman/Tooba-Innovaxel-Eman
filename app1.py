import random
import string


app = Flask(__name__)
CORS(app)

@@ -27,16 +26,6 @@ def create_short_url():
if not original_url:
return jsonify({"error": "URL is required"}), 400


       # Check if URL already exists
    existing = db.urls.find_one({"url": original_url})
    if existing:
        existing["id"] = str(existing["_id"])
        return jsonify({
            "message": "This URL has already been shortened.",
            "data": existing
        }), 200

# Generate unique short code
short_code = generate_short_code()
while db.urls.find_one({"shortCode": short_code}):
@@ -55,7 +44,7 @@ def create_short_url():

return jsonify(url_data), 201

# retrive Long Url by entring short code

@app.route('/shorten/<short_code>', methods=['GET'])
def retrieve_url(short_code):
url = db.urls.find_one({"shortCode": short_code})
@@ -66,8 +55,6 @@ def retrieve_url(short_code):
url['id'] = str(url['_id'])
return jsonify(url)


# Update Long URL based on short url
@app.route('/shorten/<short_code>', methods=['PUT'])
def update_url(short_code):
data = request.json
@@ -88,16 +75,21 @@ def update_url(short_code):
updated["id"] = str(updated["_id"])
return jsonify(updated)


@app.route('/shorten/<short_code>', methods=['DELETE'])
def delete_url(short_code):
result = db.urls.delete_one({"shortCode": short_code})
if result.deleted_count == 0:
return jsonify({"error": "Short URL not found"}), 404
return '', 204

@app.route('/shorten/<short_code>/stats', methods=['GET'])
def get_stats(short_code):
    url = db.urls.find_one({"shortCode": short_code})
    if not url:
        return jsonify({"error": "Short URL not found"}), 404

    url["id"] = str(url["_id"])
    return jsonify(url)

if __name__ == '__main__':
app.run(debug=True, port=5000)

