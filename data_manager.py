import requests

sheety_endpoint = "https://api.sheety.co/511438973b166a49328249e91a290d0c/flightDealsTracker/prices"
sheety_user_endpoint = "https://api.sheety.co/511438973b166a49328249e91a290d0c/flightDealsTracker/users"


class DataManager:
    def __init__(self):
        self.data = None
        self.prices = None
        self.iata = None
        self.dict = None
        self.user_emails = None

    def sheety_data_get(self):
        response = requests.get(url=sheety_endpoint)
        response.raise_for_status()
        self.data = response.json()["prices"]
        self.prices = [self.data[n]["lowestPrice"] for n in range(0, len(self.data))]
        self.sheety_emails()
        return self.data

    def sheety_emails(self):
        response = requests.get(url=sheety_user_endpoint)
        email_data = response.json()["users"]
        self.user_emails = [user["email"] for user in email_data]

    def sheety_update_iata(self):
        index = 2
        for iata in self.iata:
            prices = {"price": {"iataCode": f"{iata}"}}
            response = requests.put(url=f"{sheety_endpoint}/{index}", json=prices)
            response.raise_for_status()
            index += 1
        self.dict_price_iata()

    def dict_price_iata(self):
        self.dict = [{"iata": self.iata[n], "lowPrice": self.prices[n]} for n in range(0, len(self.iata))]
