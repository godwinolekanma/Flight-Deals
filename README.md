# Flight Deals Notifier

Flight Deals Notifier is a Python script designed to search for flight deals, update city data with IATA codes, and notify users about any found flight deals via email. It leverages APIs such as Sheety and Tequila (Kiwi.com) to fetch flight and city data and send email notifications.

## APIs Used

- **Sheety API**: Used to retrieve and update city data. Sheety is a platform that allows turning spreadsheets into APIs.
- **Tequila API by Kiwi.com**: Used to obtain IATA codes for cities and search for flight deals. Tequila is a flight search and booking API provided by Kiwi.com.

## Features

- Retrieves city data from Sheety API.
- Obtains IATA codes for each city using Tequila API and updates city data accordingly.
- Sets up search parameters for flight search, including origin and destination airports, date range, and price range.
- Searches for flight deals based on the defined search parameters.
- Notifies users via email about any found flight deals.

## Usage

1. Modify the search parameters in the `main.py` script to customize the flight search criteria.
2. Run the `main.py` script to start the flight deals notifier.
3. Users will be notified via email about any found flight deals that match the search criteria.