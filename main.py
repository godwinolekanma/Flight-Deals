from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from email_notification import NotificationManager

# Initialize DataManager, FlightSearch, and NotificationManager objects
dataManager = DataManager()
flight_search = FlightSearch()
email_notification = NotificationManager()

# Retrieve city data from Sheety API
city_data = dataManager.sheety_data_get()

# Get IATA codes for each city from FlightSearch API and update the city data with IATA codes
dataManager.iata = flight_search.get_iata_city(city_data)
dataManager.sheety_update_iata()

# Get user emails from city data
email_notification.email = dataManager.user_emails

# Get today's date, tomorrow's date, and six months later date
now = datetime.now()
today = now.today()
tomorrow = (today + timedelta(days=1)).strftime(f"%d/%m/%Y")
six_months_later = (today + timedelta(days=30 * 6)).strftime(f"%d/%m/%Y")

# Loop through each city in city data
for flight in dataManager.dict:
    # Set search parameters for FlightSearch API
    search_params = {
        "fly_from": "IAH",
        "fly_to": flight["iata"],
        "date_from": tomorrow,
        "date_to": six_months_later,
        "nights_in_dst_from": 2,
        "nights_in_dst_to": 30,
        "adults": 1,
        "price_from": 0,
        "price_to": flight["lowPrice"] - 1,  # Gives lowest price range value
        "curr": "USD",
        "limit": "1"
    }
    # Search for flights based on search parameters
    flight_info = flight_search.flight_finder(flight, search_params)
    # If no flights found, continue to the next city
    if flight_info is None:
        continue
    else:
        # Notify users about the found flight
        email_notification.email_users(flight_info)