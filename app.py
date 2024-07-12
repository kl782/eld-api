import json
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

geojson_data = {}
data_dir = 'data'
for filename in os.listdir(data_dir):
    if filename.endswith('.json'):
        year = filename.split('.')[0]
        with open(os.path.join(data_dir, filename), 'r') as f:
            geojson_data[year] = json.load(f)

@app.route('/api/query', methods=['GET'])
def query_geojson():
    year = request.args.get('year')
    postal_code = request.args.get('postal_code')
    
    if not year or not postal_code:
        return jsonify({"error": "Both year and postal_code are required"}), 400
    
    if year not in geojson_data:
        return jsonify({"error": f"Data for year {year} not available"}), 404
    
    results = []
    for feature in geojson_data[year]['features']:
        properties = feature.get('properties', {})
        if properties.get('postal_code') == postal_code:
            results.append(feature)
    
    if not results:
        return jsonify({"error": f"No data found for postal code {postal_code} in year {year}"}), 404
    
    return jsonify({
        "type": "FeatureCollection",
        "features": results
    })

@app.route('/api/available_years', methods=['GET'])
def get_available_years():
    return jsonify(list(geojson_data.keys()))

if __name__ == '__main__':
    app.run(debug=True)
