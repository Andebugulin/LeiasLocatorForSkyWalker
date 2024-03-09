from flask import Flask, request, jsonify
from flask_cors import CORS  
from api_functions import get_route_info, get_sun_info, get_timezone_info
import time
import datetime

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

        timestamp = int(time.time())
        timezone_info = get_timezone_info(lat, lng, timestamp)
        
        if sun_info['status'] == 'OK' and timezone_info['status'] == 'OK':
            # Convert sunrise and sunset from UTC to local time using timezone info
            local_sunrise = datetime.utcfromtimestamp(int(sun_info['results']['sunrise']) + timezone_info['dstOffset'] + timezone_info['rawOffset'])
            local_sunset = datetime.utcfromtimestamp(int(sun_info['results']['sunset']) + timezone_info['dstOffset'] + timezone_info['rawOffset'])
            
            sun_info['results']['sunrise'] = local_sunrise.strftime('%Y-%m-%d %H:%M:%S')
            sun_info['results']['sunset'] = local_sunset.strftime('%Y-%m-%d %H:%M:%S')
        # if timezone fetching wasn't successful
        return jsonify(sun_info)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)
