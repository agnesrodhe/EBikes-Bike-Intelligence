import requests
import json
import time

class MakeApiCall:

    # def get_all_bikes(self, api):
    #     response = requests.get(f"{api}")
    #     if response.status_code == 200:
    #         self.formatted_print(response.json())
    #     else:
    #         print(f"{response.status_code} error")

    def get_all_active_bikes(self, api, headers):
        response = requests.get(f"{api}/city/6378989b6a6403d2a9c6edb1/active")
        if response.status_code == 200:
            print_response = response.json()
            for j, i in enumerate(print_response):
                if ((j % 2) == 0):
                    bike_id = i.get("_id")
                    print(j, bike_id)
                    requests.put(f"{api}/{bike_id}", data = json.dumps({"active":False}), headers=headers)
                    print(i.get("active"))
                else:
                    print(i.get("active"))
        else:
            print(f"{response.status_code} error")

    def formatted_print(self, obj):
        text = json.dumps(obj, sort_keys=True, indent=4)
        return text

    # def get_one_bike(self, api):
    #     response = requests.get(f"{api}/637e34a55f990efd01cbcd8f")
    #     if response.status_code == 200:
    #         self.formatted_print(response.json())
    #     else:
    #         print(f"{response.status_code} error")

    # def update_one_bike(self, api, headers):
    #     response = requests.put(f"{api}/637e34a55f990efd01cbcd8f", data = json.dumps({"active":False}), headers=headers)
    #     if response.status_code == 200:
    #         self.formatted_print(response.json())
    #     else:
    #         print(f"{response.status_code} error")

    # def move_bike(self, api, headers):
    #     continue_move = True
    #     counter = 0
    #     coordinate1 = 15.372540927274296
    #     coordinate2 = 60.50147402944808
    #     while continue_move:
    #         counter += 1
    #         coordinate1 += 0.001
    #         if (counter == 4):
    #             continue_move = False
    #         data = json.dumps({"location": { "type": "Point", "coordinates": [coordinate1, coordinate2] }})
    #         response = requests.put(f"{api}/637e34a55f990efd01cbcd8f", data=data, headers=headers)
    #         if response.status_code == 200:
    #             self.formatted_print(response.json())
    #         else:
    #             print(f"{response.status_code} error")
    #         time.sleep(4)


    def __init__(self, api):
        headers = {'Content-Type': 'application/json'}
        self.get_all_active_bikes(api, headers)

        # self.move_bike(api, headers)

if __name__ == "__main__":
    api_call = MakeApiCall("http://localhost:3002/v1/bikes")