from flask import Flask, request, jsonify
from flask_cors import CORS  
from api_functions import get_route_info, get_sun_info

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

@app.route('/route', methods=['POST'])
def route():
    data = request.json
    origin = data['origin']
    destination = data['destination']
    try:
        route_info = get_route_info(origin, destination)
        return jsonify(route_info)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
@app.route('/sun', methods=['POST'])
def get_sun_times():
    data = request.json
    lat = data['lat']
    lng = data['lng']
    try:
        sun_info = get_sun_info(lat, lng)
        return jsonify(sun_info)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    

if __name__ == '__main__':
    app.run(debug=True)
