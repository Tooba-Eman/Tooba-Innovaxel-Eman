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
