import urllib.parse
import requests
import dotenv
import os

dotenv.load_dotenv()


# Read the number of remaining requests from a file
def number_requests_left():
    with open('requests_left.txt', 'r') as file:
        content = file.read().strip() 
        if content:
            return int(content)
        else:
            
            raise ValueError("The file is empty or contains non-numeric characters.")


# If the number of remaining requests is 0 or less, raise an error
def raise_exception_if_no_requests_left():
    nrl = number_requests_left()
    if number_requests_left() <= 0:
        raise Exception('You have reached your API call limit')

def main():
    main_api = "https://www.mapquestapi.com/directions/v2/route?"
    key = os.getenv("MAPQUEST_API_KEY")

    while True:
        raise_exception_if_no_requests_left()
        current_requests_left = number_requests_left()

        orig = input("Starting Location: ")
        if orig == "quit" or orig == "q":
            break
        dest = input("Destination: ")
        if dest == "quit" or dest == "q":
            break
        url = main_api + urllib.parse.urlencode({"key": key, "from":orig, "to":dest})

        print("URL: " + (url))
        json_data = requests.get(url).json()
        json_status = json_data["info"]["statuscode"]
    
        if json_status == 0:
             # Decrease the number of remaining requests in the variable by 1
            current_requests_left -= 1

            # Write the new number of remaining requests back to the file
            with open('requests_left.txt', 'w') as file:
                file.write(str(current_requests_left))

            print("API Status: " + str(json_status) + " = A successful route call.\n") 
            
            print("Directions from " + (orig) + " to " + (dest))
            print("Trip Duration: " + str(json_data["route"]["formattedTime"]))
            print("Kilometers: " + str("{:.2f}".format((json_data["route"]["distance"])*1.61)))
            print("=============================================")

            print("=============================================")
            for each in json_data["route"]["legs"][0]["maneuvers"]:
                print((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)"))  
                print("=============================================\n")


        elif json_status == 402:
            print("**********************************************")
            print("For Staus Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")   
            print("**********************************************\n")
            print("=============================================")
        else:
            print("************************************************************************")
            print("For Staus Code: " + str(json_status) + ", Refer to:")
            print("https://developer.mapquest.com/documentation/directions-api/status-codes")
            print("************************************************************************\n")

if __name__ == "__main__":
    main()

