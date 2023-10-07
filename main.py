import requests
import os
import pytz
from datetime import datetime, timedelta
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
WEBHOOK = os.environ["DISCORD_WEBHOOK"]
LOG_FILE = "/var/log/cron.log"
MAXIMUM_RATE = 16 # Set your desired maximum rate here.
DEBUG = os.environ.get("DEBUG", "False") == "True"

def fetch_rates():
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.get(API_ENDPOINT, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def post_to_discord(message):
    data = {
        "content": message
    }
    response = requests.post(WEBHOOK, data=data)
    return response.status_code

def control_smart_plug(action,value_inc_vat,avg_rate_next_12_hrs):
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

        # Get the last line of the log file
        try:
            with open(LOG_FILE, 'r') as f:
                last_line = f.readlines()[-1]
        except Exception as e:
            logger.error('Failed to open log file', e)
            last_line = ""

        # Control the smart plug based on the action
        if action == "on":
            plug.turnOn()
            message = f"Plug turned ON at {formatted_dt} as rate {value_inc_vat} is below {int(avg_rate_next_12_hrs)}."

            # Only alert if status changed
            if "on" in last_line:
                return
            else:
                print(message)
                status_code = post_to_discord(message)

        elif action == "off":
            plug.turnOff()
            message = f"Plug turned OFF at {formatted_dt} as rate {value_inc_vat} is above {int(avg_rate_next_12_hrs)}."

            # Only alert if status changed
            if "off" in last_line:
                return
            else:
                print(message)
                status_code = post_to_discord(message)
    except Exception as e:
        logger.error('Failed to control the smart plug: %s', e)

def convert_to_bst(utc_time_str):
    utc_time = datetime.fromisoformat(utc_time_str.replace("Z", "+00:00"))
    bst_timezone = pytz.timezone("Europe/London")
    bst_time = utc_time.astimezone(bst_timezone)
    return bst_time

def within_next_12_hours(from_time, to_time, current_time):
    twelve_hrs_later = current_time + timedelta(hours=12)
    return from_time <= twelve_hrs_later and (to_time is None or to_time > current_time)

def main():
    rates_data = fetch_rates()

    # Get current time in bst timezone
    current_time_bst = datetime.now(pytz.timezone("Europe/London"))
    
    average_rate_for_next_12_hrs = []

    for rate in rates_data["results"]:
        valid_from_bst = convert_to_bst(rate["valid_from"])
        valid_to = rate.get("valid_to", "Ongoing")

        if valid_to != "Ongoing":
            valid_to_bst = convert_to_bst(valid_to)
        else:
            valid_to_bst = None

        if within_next_12_hours(valid_from_bst, valid_to_bst, current_time_bst):
            value_inc_vat = float(rate["value_inc_vat"])  # Ensure value is a float
            average_rate_for_next_12_hrs.append(value_inc_vat)  # Add rate to list

    # Compute average if list is not empty. If calculated average is greater than MAXIMUM_RATE,
    # set avg_rate_next_12_hrs as MAXIMUM_RATE
    if average_rate_for_next_12_hrs:
        avg_rate_next_12_hrs = min(sum(average_rate_for_next_12_hrs) / len(average_rate_for_next_12_hrs), MAXIMUM_RATE)

        for rate in rates_data["results"]:
            valid_from_bst = convert_to_bst(rate["valid_from"])

            if valid_from_bst <= current_time_bst:
                valid_to = rate.get("valid_to", "Ongoing")
                
                if valid_to != "Ongoing":
                    valid_to_bst = convert_to_bst(valid_to)

                    if valid_to_bst < current_time_bst:
                        continue

                value_inc_vat = float(rate["value_inc_vat"])

                if value_inc_vat < avg_rate_next_12_hrs:
                    action = "on"
                    if DEBUG:
                        print(f"Plug turned ON as rate {value_inc_vat} is below {int(avg_rate_next_12_hrs)}.")
                    else:
                        control_smart_plug(action,value_inc_vat,avg_rate_next_12_hrs)
                else:
                    action = "off"
                    if DEBUG:
                        print(f"Plug turned OFF as rate {value_inc_vat} is above {int(avg_rate_next_12_hrs)}.")
                    else:
                        control_smart_plug(action,value_inc_vat,avg_rate_next_12_hrs)

if __name__ == "__main__":
    main()