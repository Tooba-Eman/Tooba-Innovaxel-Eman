url_data["id"] = str(inserted.inserted_id)

return jsonify(url_data), 201

# retrive Long Url by entring short code
@app.route('/shorten/<short_code>', methods=['GET'])
def retrieve_url(short_code):
    url = db.urls.find_one({"shortCode": short_code})
    if not url:
        return jsonify({"error": "Short URL not found"}), 404

    db.urls.update_one({"shortCode": short_code}, {"$inc": {"accessCount": 1}})
    url['id'] = str(url['_id'])
    return jsonify(url)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

