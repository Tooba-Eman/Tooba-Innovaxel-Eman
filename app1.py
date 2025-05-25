url['id'] = str(url['_id'])
return jsonify(url)


# Update Long URL based on short url
@app.route('/shorten/<short_code>', methods=['PUT'])
def update_url(short_code):
    data = request.json
    new_url = data.get("url")
    if not new_url:
        return jsonify({"error": "URL is required"}), 400

    url = db.urls.find_one({"shortCode": short_code})
    if not url:
        return jsonify({"error": "Short URL not found"}), 404

    db.urls.update_one(
        {"shortCode": short_code},
        {"$set": {"url": new_url, "updatedAt": datetime.utcnow().isoformat()}}
    )

    updated = db.urls.find_one({"shortCode": short_code})
    updated["id"] = str(updated["_id"])
    return jsonify(updated)

if __name__ == '__main__':
app.run(debug=True, port=5000)
