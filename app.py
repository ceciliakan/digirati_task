"""
curl -X POST -H "Content-Type: application/json" -d '{"key": "value"}' http://127.0.0.1:5000/process_json
"""

import json
from flask import Flask, request, jsonify

from src.scrape_url import scrape_text_from_url
from src.ner import ner_model, collect_entities

app = Flask(__name__)

@app.route('/process_json', methods=['POST'])
def process_json():
    if request.method == 'POST':
        data = request.get_json()
        url_to_scrape = data.get("URL", None)

        if url_to_scrape:
            response = scrape_text_from_url(url_to_scrape)

            if response["error"]:
                return response["message"]
            else:
                doc = ner_model(response["message"])
                entities = collect_entities(doc)
                data.update({"people": entities})

                return jsonify(data)
        else:
            return "Missing URL"
    else:
        return "Invalid request method"

if __name__ == '__main__':
    app.run(debug=True)


