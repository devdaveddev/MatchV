
from flask import Flask, request, jsonify
from engine import search_names, add_person
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  

@app.route("/search", methods=["GET"])
def search_api():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify(error="provide ?q=name"), 400
    
    print(f"Search query received: {query}")
    
    results = search_names(query, top_k=10)
    print(f"Search response: {results}")
    return jsonify({'results':results})


@app.route("/add", methods=["POST"])
def add_person_api():
    data = request.get_json() or {}
    try:
        new = add_person(data)
        return jsonify(success=True, person=new), 201
    except ValueError as e:
        return jsonify(error=str(e)), 400


if __name__ == "__main__":
    print("Backend running at http://127.0.0.1:5000")
    app.run(debug=True)
