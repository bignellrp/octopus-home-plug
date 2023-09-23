import requests
import os
import pytz
from datetime import datetime
from PyP100 import PyP100
from dotenv import load_dotenv
import logging

# Load values from .env
load_dotenv()

# Access the API key
API_KEY = os.environ["OCTOPUS_API_KEY"]

BASEURL = "https://api.octopus.energy"
PRODUCT = "AGILE-FLEX-22-11-25"
TARIFF = "E-1R-AGILE-FLEX-22-11-25-B"
API_ENDPOINT = f"{BASEURL}/v1/products/{PRODUCT}/electricity-tariffs/{TARIFF}/standard-unit-rates/"
EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]
SMART_PLUG_IP = os.environ["SMART_PLUG_IP"]

def fetch_rates():
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.get(API_ENDPOINT, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def control_smart_plug(action):
    # Create a logger
    logger = logging.getLogger(__name__)

    try:
        # Create a P100 plug object
        plug = PyP100.P100(SMART_PLUG_IP, EMAIL, PASSWORD)

        plug.handshake() #Creates the cookies required for further methods
        plug.login() #Sends credentials to the plug and creates AES Key and IV for further methods

        # Get current time in bst timezone
        current_time_bst = datetime.now(pytz.timezone("Europe/London"))

        # Parse into a datetime object
        dt = datetime.fromisoformat(str(current_time_bst))

        # Format the datetime object
        formatted_dt = dt.strftime("%Y-%m-%d %H:%M")

        # Control the smart plug based on the action
        if action == "on":
            plug.turnOn()
            print(f"Turned on the smart plug at {formatted_dt} due to low rate.")
        elif action == "off":
            plug.turnOff()
            print(f"Turned off the smart plug at {formatted_dt} due to high rate.")
    except Exception as e:
        logger.error('Failed to control the smart plug: %s', e)

def convert_to_bst(utc_time_str):
    utc_time = datetime.fromisoformat(utc_time_str.replace("Z", "+00:00"))
    bst_timezone = pytz.timezone("Europe/London")
    bst_time = utc_time.astimezone(bst_timezone)
    return bst_time

def main():
    rates_data = fetch_rates()

    # Get current time in bst timezone
    current_time_bst = datetime.now(pytz.timezone("Europe/London"))

    for rate in rates_data["results"]:
        valid_from_bst = convert_to_bst(rate["valid_from"])

        # Compare rate's validity period with the current time
        if valid_from_bst <= current_time_bst:
            valid_to = rate.get("valid_to", "Ongoing")
            
            if valid_to != "Ongoing":
                valid_to_bst = convert_to_bst(valid_to)

                # If the rate is expired then skip this iteration
                if valid_to_bst < current_time_bst:
                    continue

            value_inc_vat = float(rate["value_inc_vat"])  # Ensure value is a float for comparison
        
            # Control the smart plug based on the rate
            if value_inc_vat < 18.0:
                action = "on"
                control_smart_plug(action)
                print(f"Rate : {value_inc_vat} p/kWh.")
            else:
                action = "off"
                control_smart_plug(action)
                print(f"Rate : {value_inc_vat} p/kWh.")

if __name__ == "__main__":
    main()