import json
import os
from flask import Flask, jsonify, request
import requests
from shapely.geometry import Point, Polygon

app = Flask(__name__)

# Load GeoJSON data
geojson_data = {}
data_dir = 'data'
for filename in os.listdir(data_dir):
    if filename.endswith('.json'):
        year = filename.split('.')[0]
        with open(os.path.join(data_dir, filename), 'r') as f:
            geojson_data[year] = json.load(f)

def get_coordinates_for_postal_code(postal_code):
    url = f"https://www.onemap.gov.sg/api/common/elastic/search?searchVal={postal_code}&returnGeom=Y&getAddrDetails=N"
    response = requests.get(url)
    if response.status_code == 200:
      x = response.json()
      lat = x['results'][0]['LATITUDE']
      lon = x['results'][0]['LONGITUDE']
      return(lat,lon)
    else:
      print("Error fetching coordinates")

def point_in_polygon(point, polygon):
    return Polygon(polygon).contains(Point(point))

@app.route('/api/query', methods=['GET'])
def query_electoral_division():
    postal_code = request.args.get('postal_code')
    year = request.args.get('year', max(geojson_data.keys())) 
    
    if not postal_code:
        return jsonify({"error": "Postal code is required"}), 400
    
    if year not in geojson_data:
        return jsonify({"error": f"Data for year {year} not available"}), 404

    # Step 1: Get coordinates for the postal code
    try:
        lon, lat = get_coordinates_for_postal_code(postal_code)
    except Exception as e:
        return jsonify({"error": f"Failed to get coordinates for postal code: {str(e)}"}), 500

    # Step 2: Determine electoral boundary
    for feature in geojson_data[year]['features']:
        polygon = feature['geometry']['coordinates'][0]
        if point_in_polygon((lon, lat), polygon):
            properties = feature['properties']
            ed_code = properties['Description'].split('ED_CODE</th> <td>')[1].split('</td>')[0]
            ed_desc = properties['Description'].split('ED_DESC</th> <td>')[1].split('</td>')[0].strip()
            return jsonify({
                "postal_code": postal_code,
                "year": year,
                "ed_code": ed_code,
                "ed_desc": ed_desc,
                "coordinates": {"lon": lon, "lat": lat}
            })

    return jsonify({"error": "No electoral division found for the given postal code"}), 404

@app.route('/api/available_years', methods=['GET'])
def get_available_years():
    return jsonify(list(geojson_data.keys()))

if __name__ == '__main__':
    app.run(debug=True)
