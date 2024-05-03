import requests
import os

tequila_location_endpoint = "https://api.tequila.kiwi.com/locations/query"
tequila_search_endpoint = "https://api.tequila.kiwi.com/v2/search"
TEQ_API_KEY = os.environ.get("TEQ_API_KEY")


class FlightSearch:
    def __init__(self):
        self.info = None
        self.header = {"apikey": TEQ_API_KEY}
        self.iata_list = []

    def get_iata_city(self, city_data):
        for n in range(0, len(city_data)):
            city = city_data[n]["city"]
            params = {
                "term": city,
                "location_types": "airport",
                "limit": 1,
            }
            response = requests.get(url=tequila_location_endpoint, headers=self.header, params=params)
            response.raise_for_status()
            # iata response id
            iata = response.json()["locations"][0]["id"]
            self.iata_list.append(iata)
        return self.iata_list

    def flight_finder(self, flight, search_params):
        # check dictionary price doesn't have negative value and pass to next dict if it does
        if flight["lowPrice"] <= 1:
            pass
        else:
            # tequila_search_endpoint parameters using google sheets determined price
            response = requests.get(url=tequila_search_endpoint, headers=self.header, params=search_params)
            response.raise_for_status()
            direct_data = response.json()["data"]
            # if data empty - increase stopover by 1
            if not direct_data:
                search_params["max_stopovers"] = 1
                new_response = requests.get(url=tequila_search_endpoint, headers=self.header, params=search_params)
                NEW_DATA = new_response.json()["data"]
                if not NEW_DATA:
                    pass
                else:
                    print(NEW_DATA)
                    going_data = NEW_DATA[0]
                    return_data = NEW_DATA[0]["route"][-1]
                    self.info = (f"Low price alert! Only {int(going_data["price"])} to fly from "
                                 f"{going_data["cityFrom"]}-{going_data["flyFrom"]} to "
                                 f"{going_data["cityTo"]}-{going_data["flyTo"]}, from "
                                 f"{str(going_data["local_departure"]).split("T")[0]} to "
                                 f"{return_data["local_departure"].split("T")[0]}.")
                    return self.info

            # put flight data values in a new dict
            else:
                going_data = direct_data[0]
                return_data = direct_data[0]["route"][-1]  # search end of list for return data
                self.info = f'Low price alert! Only {int(going_data["price"])} to fly from ' \
                            f'{going_data["cityFrom"]}-{going_data["flyFrom"]} to ' \
                            f'{going_data["cityTo"]}-{going_data["flyTo"]}, from ' \
                            f'{str(going_data["local_departure"]).split("T")[0]} to ' \
                            f'{return_data["local_departure"].split("T")[0]}.'
                return self.info
