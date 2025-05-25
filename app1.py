url_data["id"] = str(inserted.inserted_id)

return jsonify(url_data), 201
# @app.route('/shorten', methods=['POST'])
# def create_short_url():
#     data = request.json
#     original_url = data.get('url')
#     if not original_url:
#         return jsonify({"error": "URL is required"}), 400


#        # Check if URL already exists
#     existing = db.urls.find_one({"url": original_url})
#     if existing:
#         existing["id"] = str(existing["_id"])
#         return jsonify({
#             "message": "This URL has already been shortened.",
#             "data": existing
#         }), 200

#     # Generate unique short code
#     short_code = generate_short_code()
#     while db.urls.find_one({"shortCode": short_code}):
#         short_code = generate_short_code()

#     now = datetime.utcnow().isoformat()
#     url_data = {
#         "url": original_url,
#         "shortCode": short_code,
#         "createdAt": now,
#         "updatedAt": now,
#         "accessCount": 0
#     }
#     inserted = db.urls.insert_one(url_data)
#     url_data["id"] = str(inserted.inserted_id)

#     return jsonify(url_data), 201


@app.route('/shorten/<short_code>', methods=['GET'])
@@ -154,5 +120,14 @@ def get_stats(short_code):
url["id"] = str(url["_id"])
return jsonify(url)

@app.route('/r/<short_code>')
def redirect_short_url(short_code):
    url = db.urls.find_one({"shortCode": short_code})
    if not url:
        return render_template('404.html'), 404

    db.urls.update_one({"shortCode": short_code}, {"$inc": {"accessCount": 1}})
    return redirect(url['url'])

if __name__ == '__main__':
app.run(debug=True, port=5000)
