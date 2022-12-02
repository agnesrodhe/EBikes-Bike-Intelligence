import requests
import json
import random


API = "http://localhost:3002/v1"
HEADERS = {'Content-Type': 'application/json'}
CITY = "637e2a5a22f175ffd136d0d7"

FIRSTNAMES = ["Alice", "Noah", "Maja", "William", "Vera", "Liam", "Alma", "Hugo"]
LASTNAMES = ["Viklund", "Eliasson", "Holmgren", "Blom", "Andersson", "Skog", "Lind", "Sten"]


def add_users():
    """Add users"""
    amount = 0
    users = dict()
    while amount < 20:
        fName = random.choice(FIRSTNAMES)
        lName = random.choice(LASTNAMES)
        uName = (fName + lName).lower()
        users[uName] = [fName, lName, uName]
        amount = amount + 1

    for i in users:
        password = i + str(random.randrange(100, 1000))
        users[i].append(password)
        data = json.dumps({"firstName": users[i][0], "lastName": users[i][1], "username": users[i][2], "password": users[i][3], "role": "customer" })
        response = requests.post(f"{API}/user/signUp", data=data, headers=HEADERS)
        print_response = response.json()
        print(print_response)


def add_active_bikes(longmin, longmax, latmin, latmax):
    """Add active bikes that is working"""
    named = "BorlängeBike-"
    users = requests.get(f"{API}/user/allCustomers")
    users_json = users.json()
    number_bikes = get_number_of_bikes_in_city()
    amount = 20
    for i in range(amount):
        lat = random.uniform(latmax, latmin)
        long = random.uniform(longmax, longmin)
        name = named + str(number_bikes + i)
        if users_json[i].get("username") != "kund" and users_json[i].get("username") != "admin":
            user_id = users_json[i].get("_id")
            status = "working"
            charging = None
            parked = None
            maxspeed = 30
            speed = 0
            batterlevel = 100
            location = {
                "type": "Point",
                "coordinates": [
                    long,
                    lat
                ]
            }
            goal = None
            data = json.dumps({ "name": name, "active": user_id, "status": status, "charging": charging, "parked": parked, "maxspeed": maxspeed, "speed": speed, "batterylevel": batterlevel, "location": location, "inCity": CITY, "goal": goal })
            response = requests.post(f"{API}/bikes", data=data, headers=HEADERS)
            print_response = response.json()
            print(print_response)


def add_non_active_working_bikes_parking_lot():
    """Add non-active working bikes parked at a parking lot"""
    named = "BorlängeBike-"
    city = "637e2a5a22f175ffd136d0d7"
    parkstations = ["6389c3df3afbc6e3e2a1969e", "6389c3df3afbc6e3e2a1969b", "6389c3df3afbc6e3e2a19698", "6389c3de3afbc6e3e2a19694", "6389c3db3afbc6e3e2a1968d"]
    number_bikes = get_number_of_bikes_in_city()
    amount = 5
    for i in range(amount):
        name = named + str(number_bikes + i)
        parking = random.choice(parkstations)
        location = requests.get(f"{API}/parking/{parking}")
        location_type = location.json().get("location").get("type")
        location_coordinates = location.json().get("location").get("coordinates")
        data = json.dumps({ "name": name, "active": None, "status": "working", "charging": None, "parked": parking, "maxspeed": 30, "speed": 0, "batterylevel": 80, "location": {
                "type": location_type,
                "coordinates": location_coordinates
            }, "inCity": city, "goal": None })
        response = requests.post(f"{API}/bikes", data=data, headers=HEADERS)
        print_response = response.json()
        print(print_response)

def add_non_active_working_bikes_free_parking(longmin, longmax, latmin, latmax):
    """Add non-active working bikes parked at a free parking"""
    named = "BorlängeBike-"
    city = "637e2a5a22f175ffd136d0d7"
    number_bikes = get_number_of_bikes_in_city()
    amount = 5
    for i in range(amount):
        lat = random.uniform(latmax, latmin)
        long = random.uniform(longmax, longmin)
        name = named + str(number_bikes + i)
        data = json.dumps({ "name": name, "active": None, "status": "working", "charging": None, "parked": None, "maxspeed": 30, "speed": 0, "batterylevel": 60, "location": {
                "type": "Point",
                "coordinates": [
                    long,
                    lat
                ]
            }, "inCity": city, "goal": None })
        response = requests.post(f"{API}/bikes", data=data, headers=HEADERS)
        print_response = response.json()
        print(print_response)

def add_non_active_bikes_charging():
    """Add non-active bikes that is on charging station"""
    named = "BorlängeBike-"
    city = "637e2a5a22f175ffd136d0d7"
    charging_stations = ["6389c2b5c91d95b9359c65ee", "6389c2b5c91d95b9359c65eb", "6389c2b4c91d95b9359c65e8", "6389c2b4c91d95b9359c65e4", "6389c2afc91d95b9359c65dd"]
    number_bikes = get_number_of_bikes_in_city()
    amount = 5
    for i in range(amount):
        name = named + str(number_bikes + i)
        charge_station = random.choice(charging_stations)
        location = requests.get(f"{API}/chargestations/{charge_station}")
        location_type = location.json().get("location").get("type")
        location_coordinates = location.json().get("location").get("coordinates")
        data = json.dumps({ "name": name, "active": None, "status": "noBattery", "charging": charge_station, "parked": None, "maxspeed": 30, "speed": 0, "batterylevel": 30, "location": {
                "type": location_type,
                "coordinates": location_coordinates
            }, "inCity": city, "goal": None })
        response = requests.post(f"{API}/bikes", data=data, headers=HEADERS)
        print_response = response.json()
        print(print_response)

def add_non_active_not_working_bikes_parking_lot():
    """Add non-active non-working bikes parked at a parking lot"""
    named = "BorlängeBike-"
    city = "637e2a5a22f175ffd136d0d7"
    parkstations = ["6389c3df3afbc6e3e2a1969e", "6389c3df3afbc6e3e2a1969b", "6389c3df3afbc6e3e2a19698", "6389c3de3afbc6e3e2a19694", "6389c3db3afbc6e3e2a1968d"]
    number_bikes = get_number_of_bikes_in_city()
    amount = 5
    for i in range(amount):
        name = named + str(number_bikes + i)
        parking = random.choice(parkstations)
        location = requests.get(f"{API}/parking/{parking}")
        location_type = location.json().get("location").get("type")
        location_coordinates = location.json().get("location").get("coordinates")
        data = json.dumps({ "name": name, "active": None, "status": "needService", "charging": None, "parked": parking, "maxspeed": 30, "speed": 0, "batterylevel": 80, "location": {
                "type": location_type,
                "coordinates": location_coordinates
            }, "inCity": city, "goal": None })
        response = requests.post(f"{API}/bikes", data=data, headers=HEADERS)
        print_response = response.json()
        print(print_response)

def get_number_of_bikes_in_city():
    """Returns number of bikes in city"""
    bikes = requests.get(f"{API}/bikes/city/{CITY}")
    number_of_bikes = len(bikes.json())
    return number_of_bikes

if __name__ == "__main__":
    # kör funktion för att lägga till data i databasen
    # add_users()
    # add_active_bikes(15.36, 15.43, 60.46, 60.51)
    # add_non_active_working_bikes_parking_lot()
    # add_non_active_working_bikes_free_parking(15.36, 15.43, 60.46, 60.51)
    # add_non_active_bikes_charging()
    # add_non_active_not_working_bikes_parking_lot()
    print("no function choosen")