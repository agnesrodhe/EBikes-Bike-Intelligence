"""
Module for a bike simulation program
"""

import requests
import time
import random
import json



API = "http://server:3002/v1/bikes"
HEADERS = {'Content-Type': 'application/json'}
CITY = "637e2a5a22f175ffd136d0d7"
CITY_LONGMIN = 15.36
CITY_LONGMAX = 15.43
CITY_LATMIN = 60.46
CITY_LATMAX = 60.51
# GOAL_LONGMIN = 15.37
# GOAL_LONGMAX = 15.42
# GOAL_LATMIN = 60.47
# GOAL_LATMAX = 60.50
# VERSION 1
# Hämta aktiva cyklar
# loopa igenom alla aktiva cyklar
# fortsätt med cyklar med status working
# om cykeln är inom stadens område fortsätt
# om cykeln inte har ett mål - sätt ett mål annars fortsätt
# uppdatera positionen
# uppdatera hastighet
# uppdatera batterinivån
# kolla om cykelns batteri är för lågt => ändra status

# VERSION 2
# Hämta aktiva cyklar sortera ut de som inte är inom staden och sätt dom till status: outsideCity
# loopa igenom alla aktiva cyklar
# fortsätt med cyklar med status working
# om cykeln inte har ett mål - sätt ett mål annars fortsätt
# uppdatera positionen
# uppdatera hastighet
# uppdatera batterinivån
# kolla om cykelns batteri är för lågt => ändra status

# VERSION 3
# Hämta aktiva cyklar
# loopa igenom alla aktiva cyklar
# fortsätt med cyklar med status working
# uppdatera positionen
#   om cykeln inte har ett mål - sätt ett mål
#   om cykelns position är utanför staden byt mål
#   annars uppdatera position mot målet
# uppdatera hastighet
# uppdatera batterinivån
# kolla om cykelns batteri är för lågt => ändra status

def main():
    """Function to start the simulation"""
    counter = 0
    while True:
        active_bikes = get_all_active_bikes()
        for index, bike in enumerate(active_bikes):
            if bike['status'] == "working":
                check_goal_and_update(bike)
                update_speed(bike)
                if counter % 5 == 0:
                    print("battery lower")
                    # lower_battery(bike)
                if bike.get("batterylevel") < 10:
                    set_bike_to_not_working(bike)
        counter += 1
        if counter > 5:
            break
        time.sleep(2)

def get_all_active_bikes():
    """Function returns all active bikes in a city"""
    response = requests.get("{0}/city/{1}/active".format(API, CITY))
    if response.status_code == 200:
        print_response = response.json()
        return print_response
    else:
        print("{} error".format(response.status_code))

def set_goal_for_bike(bike):
    """Function sets a goal for a bike"""
    lat = random.uniform(CITY_LATMAX, CITY_LATMIN)
    long = random.uniform(CITY_LONGMAX, CITY_LONGMIN)
    goal = { "goal": { "type": "Point", "coordinates": [ long, lat ] } }
    requests.put("{0}/{1}".format(API, bike['_id']), data = json.dumps(goal), headers=HEADERS)

def check_goal_and_update(bike):
    """Function checks goal and updates a bike position depending on the goal"""
    if bike.get("goal") == None:
        set_goal_for_bike(bike)
        bike_id = bike["_id"]
        response = requests.get("{0}/{1}".format(API, bike_id))
        bike = response.json()
    bike_long = bike.get("location").get("coordinates")[0]
    bike_lat = bike.get("location").get("coordinates")[1]
    if CITY_LONGMAX > bike_long > CITY_LONGMIN and CITY_LATMAX > bike_lat > CITY_LATMIN:
        print("Bike old goal", bike["name"])
        update_position(bike, 0.0001)
    else:
        print("Bike new goal", bike["goal"])
        print("Bike location", bike["location"])
        set_goal_for_bike(bike)
        bike_id = bike["_id"]
        response = requests.get("{0}/{1}".format(API, bike_id))
        bike = response.json()
        update_position(bike, 0.001)

def update_speed(bike):
    """Function to update speed on bike"""
    speed = 0
    if bike.get("speed") == 0 or bike.get("speed") == None:
        speed = 20
    data = json.dumps({ "speed": speed })
    requests.put("{0}/{1}".format(API, bike['_id']), data=data, headers=HEADERS)

def update_position(bike, movement_size):
    """Function to update position on bike"""
    goal_long = bike.get("goal").get("coordinates")[0]
    goal_lat = bike.get("goal").get("coordinates")[1]
    bike_long = bike.get("location").get("coordinates")[0]
    bike_lat = bike.get("location").get("coordinates")[1]
    difference_long = bike_long - goal_long
    difference_lat = bike_lat - goal_lat
    coordinate1 = bike_long 
    coordinate2 = bike_lat
    if difference_long > 0:
        if difference_lat > 0:
            coordinate1 = coordinate1 - movement_size
            coordinate2 = coordinate2 - movement_size
            print("snett nedåt åt vänster")
        elif difference_lat < 0:
            coordinate1 = coordinate1 - movement_size
            coordinate2 = coordinate2 + movement_size
            print("snett uppåt åt vänster")
        else:
            coordinate1 = coordinate1 - movement_size
            print("rakt åt vänster")
    elif difference_long < 0:
        if difference_lat > 0:
            coordinate1 = coordinate1 + movement_size
            coordinate2 = coordinate2 - movement_size
            print("snett nedåt åt höger")
        elif difference_lat < 0:
            coordinate1 = coordinate1 + movement_size
            coordinate2 = coordinate2 + movement_size
            print("snett uppåt åt höger")
        else:
            coordinate1 = coordinate1 + movement_size
            print("rakt åt höger")
    elif difference_long == 0:
        if difference_lat > 0:
            coordinate2 = coordinate2 - movement_size
            print("rakt nedåt")
        elif difference_lat < 0:
            coordinate2 = coordinate2 + movement_size
            print("rakt uppåt")
    data = json.dumps({"location": { "type": "Point", "coordinates": [ coordinate1, coordinate2 ] }})
    requests.put("{0}/{1}".format(API, bike['_id']), data=data, headers=HEADERS)

def lower_battery(bike):
    """Function to lower the battery on an active bike"""
    newBatteryLevel = bike["batterylevel"] - 1
    print(newBatteryLevel)
    data = json.dumps({ "batterylevel": newBatteryLevel })
    requests.put("{0}/{1}".format(API, bike['_id']), data=data, headers=HEADERS)

def set_bike_to_not_working(bike):
    """Function to update bike so that it is not working"""
    data = json.dumps({ "status": "noBattery" })
    requests.put("{0}/{1}".format(API, bike['_id']), data=data, headers=HEADERS)

if __name__ == "__main__":
    main()
