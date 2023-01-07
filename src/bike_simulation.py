"""
Module for a bike simulation program
"""

import requests
import time
import random
import json



API = "http://server:3002/v1/bikes"
HEADERS = {'Content-Type': 'application/json'}
# CITY = "637e2a5a22f175ffd136d0d7"
# city_longmin = 15.36
# city_longmax = 15.43
# city_latmin = 60.46
# city_latmax = 60.51
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
    print("")
    print("What city do you want to see?")
    print("1 - Borlänge")
    print("2 - Visby")
    print("3 - Lund")
    print("")
    choosen_city = input("Choose a number: \n")
    if choosen_city == "1":
        city = "637e2a5a22f175ffd136d0d7"
        city_longmin = 15.36
        city_longmax = 15.43
        city_latmin = 60.46
        city_latmax = 60.51
    elif choosen_city == "2":
        city = "6378989b6a6403d2a9c6edb1"
        city_longmin = 18.29
        city_longmax = 18.35
        city_latmin = 57.61
        city_latmax = 57.64
    elif choosen_city == "3":
        city = "637c7018050e0887ebe8b491"
        city_longmin = 13.12
        city_longmax = 13.29
        city_latmin = 55.66
        city_latmax = 55.73
    else:
        print("Not a valid city, start over with command: python3 bike_simulation.py")
    while True:
        active_bikes = get_all_active_bikes(city)
        for index, bike in enumerate(active_bikes):
            inUseBikes = requests.get("{0}/city/{1}/inuse".format(API, city))
            if inUseBikes.status_code == 200:
                for inUseB in inUseBikes.json():
                    check_goal_and_update(inUseB, city_longmax, city_longmin, city_latmax, city_latmin, 0.00001, 0.001)
                    update_speed(inUseB)
                    if bike.get("batterylevel") < 10:
                        set_bike_to_not_working(inUseB)
            if bike['status'] == "working":
                check_goal_and_update(bike, city_longmax, city_longmin, city_latmax, city_latmin, 0.0001, 0.001)
                update_speed(bike)
                if bike.get("batterylevel") < 10:
                    set_bike_to_not_working(bike)
            if counter % 10 == 0:
                print("battery lower")
        counter += 1
        # if counter > 20:
        #     break


def get_all_active_bikes(city):
    """Function returns all active bikes in a city"""
    response = requests.get("{0}/city/{1}/active".format(API, city))
    if response.status_code == 200:
        print_response = response.json()
        return print_response
    else:
        print("{} error".format(response.status_code))

def set_goal_for_bike(bike, city_longmax, city_longmin, city_latmax, city_latmin):
    """Function sets a goal for a bike"""
    lat = random.uniform(city_latmax, city_latmin)
    long = random.uniform(city_longmax, city_longmin)
    goal = { "goal": { "type": "Point", "coordinates": [ long, lat ] } }
    requests.put("{0}/{1}".format(API, bike['_id']), data = json.dumps(goal), headers=HEADERS)

def check_goal_and_update(bike, city_longmax, city_longmin, city_latmax, city_latmin, old_goal_dictance, new_goal_distance):
    """Function checks goal and updates a bike position depending on the goal"""
    if bike.get("goal") == None:
        set_goal_for_bike(bike, city_longmax, city_longmin, city_latmax, city_latmin)
        bike_id = bike["_id"]
        response = requests.get("{0}/{1}".format(API, bike_id))
        bike = response.json()
    bike_long = bike.get("location").get("coordinates")[0]
    bike_lat = bike.get("location").get("coordinates")[1]
    if city_longmax > bike_long > city_longmin and city_latmax > bike_lat > city_latmin:
        # print("Bike old goal", bike["name"])
        update_position(bike, old_goal_dictance)
    else:
        # print("Bike new goal", bike["goal"])
        # print("Bike location", bike["location"])
        set_goal_for_bike(bike, city_longmax, city_longmin, city_latmax, city_latmin)
        bike_id = bike["_id"]
        response = requests.get("{0}/{1}".format(API, bike_id))
        bike = response.json()
        update_position(bike, new_goal_distance)

def update_speed(bike):
    """Function to update speed on bike"""
    data = json.dumps({ "speed": 20 })
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
            # print("snett nedåt åt vänster")
        elif difference_lat < 0:
            coordinate1 = coordinate1 - movement_size
            coordinate2 = coordinate2 + movement_size
            # print("snett uppåt åt vänster")
        else:
            coordinate1 = coordinate1 - movement_size
            # print("rakt åt vänster")
    elif difference_long < 0:
        if difference_lat > 0:
            coordinate1 = coordinate1 + movement_size
            coordinate2 = coordinate2 - movement_size
            # print("snett nedåt åt höger")
        elif difference_lat < 0:
            coordinate1 = coordinate1 + movement_size
            coordinate2 = coordinate2 + movement_size
            # print("snett uppåt åt höger")
        else:
            coordinate1 = coordinate1 + movement_size
            # print("rakt åt höger")
    elif difference_long == 0:
        if difference_lat > 0:
            coordinate2 = coordinate2 - movement_size
            # print("rakt nedåt")
        elif difference_lat < 0:
            coordinate2 = coordinate2 + movement_size
            # print("rakt uppåt")
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
