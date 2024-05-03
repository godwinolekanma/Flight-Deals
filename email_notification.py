import os

import requests
import smtplib
from data_manager import DataManager

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")


class NotificationManager:
    def __init__(self):
        self.email = None

    def email_users(self, flight_info):
        connection = smtplib.SMTP(host="smtp.gmail.com", port=587)
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        for mail in self.email:
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=mail,
                msg=f"Subject:Flight Deals on KIWI.com\n\n{flight_info}"
            )
