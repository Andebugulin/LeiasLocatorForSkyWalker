import urllib.parse
import requests
import os
import dotenv

# Load environment variables
dotenv.load_dotenv()

# Helper function to read the number of remaining requests
def number_requests_left():
    with open('requests_left.txt', 'r') as file:
        content = file.read().strip()
        if content:
            return int(content)
        else:
            raise ValueError("The file is empty or contains non-numeric characters.")

# Function to update the number of requests left
def update_requests_left(new_value):
    with open('requests_left.txt', 'w') as file:
        file.write(str(new_value))

# Main function modified to work with parameters and return data
def get_route_info(orig, dest):
    main_api = "https://www.mapquestapi.com/directions/v2/route?"
    key = os.getenv("MAPQUEST_API_KEY")

    # Check if there are requests left
    current_requests_left = number_requests_left()
    if current_requests_left <= 0:
        raise Exception('You have reached your API call limit')

    # Construct the request URL
    url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest})
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    # Decrease the number of remaining requests and update the file
    current_requests_left -= 1
    update_requests_left(current_requests_left)

    # Handle the response
    if json_status == 0:
        # Successfully retrieved route information
        directions = [{
            "narrative": maneuver["narrative"],
            "distance": "{:.2f} km".format(maneuver["distance"] * 1.61)
        } for maneuver in json_data["route"]["legs"][0]["maneuvers"]]
        
        route_info = {
            "status": "success",
            "directions": directions,
            "formattedTime": json_data["route"]["formattedTime"],
            "distance": "{:.2f} km".format(json_data["route"]["distance"] * 1.61)
        }
        return route_info
    elif json_status == 402:
        # Invalid user inputs
        return {"status": "error", "message": "Invalid user inputs for one or both locations."}
    else:
        # Other errors
        return {"status": "error", "message": f"Status Code: {json_status}. Refer to the MapQuest API documentation for details."}
