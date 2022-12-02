"""
Module for a bike simulation program
"""

import sys
import requests

API = "http://localhost:3002/v1/bikes"
HEADERS = {'Content-Type': 'application/json'}
CITY = "6378989b6a6403d2a9c6edb1"

def main():
    """Function to start the simulation"""
    counter = 0
    while counter < 4:
        active_bikes = get_all_active_bikes(API, CITY)
        for bike in active_bikes:
            if bike.works == True:
                if bike.get("goal") == "null":
                    set_goal_for_bike(bike)
                update_position(bike)
                update_speed(bike)
                lower_battery(bike)
                if bike.get("batterylevel") < 5:
                    set_bike_to_not_working(bike)
        counter += 1


def get_all_active_bikes(api, city):
    """Function returns all active bikes in a city"""
    response = requests.get(f"{api}/city/{city}/active")
    if response.status_code == 200:
        print_response = response.json()
        return print_response
    else:
        print(f"{response.status_code} error")

def set_goal_for_bike(bike):
    """Function sets a goal for a bike"""

def update_position(bike):
    """Function updates a bikes position depending on the goal"""

def update_speed(bike):
    """Function to update speed on bike"""

def lower_battery(bike):
    """Function to lower the battery on an active bike"""

def set_bike_to_not_working(bike):
    """Function to update bike so that it is not working"""

if __name__ == "__main__":
    main()
