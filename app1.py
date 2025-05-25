updated["id"] = str(updated["_id"])
return jsonify(updated)


@app.route('/shorten/<short_code>', methods=['DELETE'])
def delete_url(short_code):
    result = db.urls.delete_one({"shortCode": short_code})
    if result.deleted_count == 0:
        return jsonify({"error": "Short URL not found"}), 404
    return '', 204


if __name__ == '__main__':
app.run(debug=True, port=5000)
