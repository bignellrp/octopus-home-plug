import requests
import os
from dotenv import load_dotenv
import pytz
from datetime import datetime
from kasa import SmartPlug

# Load values from .env
load_dotenv()

# Access the API key
API_KEY = os.environ["OCTOPUS_API_KEY"]

BASEURL = "https://api.octopus.energy"
PRODUCT = "AGILE-FLEX-22-11-25"
TARIFF = "E-1R-AGILE-FLEX-22-11-25-B"
API_ENDPOINT = f"{BASEURL}/v1/products/{PRODUCT}/electricity-tariffs/{TARIFF}/standard-unit-rates/"

def fetch_rates():
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.get(API_ENDPOINT, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

SMART_PLUG_IP = os.environ["SMART_PLUG_IP"]

async def control_smart_plug(rate):
    plug = SmartPlug(SMART_PLUG_IP)
    await plug.update()

    if rate < 18:
        if not plug.is_on:
            await plug.turn_on()
            print("Turning on the smart plug due to low rate.")
    elif rate >= 18:
        if plug.is_on:
            await plug.turn_off()
            print("Turning off the smart plug due to high rate.")

def convert_to_bst(utc_time_str):
    utc_time = datetime.fromisoformat(utc_time_str.replace("Z", "+00:00"))
    bst_timezone = pytz.timezone("Europe/London")
    bst_time = utc_time.astimezone(bst_timezone)
    return bst_time

def main():
    rates_data = fetch_rates()
    
    for rate in rates_data["results"]:
        valid_from_bst = convert_to_bst(rate["valid_from"])
        
        valid_to = rate.get("valid_to", "Ongoing")
        if valid_to != "Ongoing":
            valid_to_bst = convert_to_bst(valid_to)
            valid_to_str = valid_to_bst.strftime('%Y-%m-%dT%H:%M:%S%z')
        else:
            valid_to_str = "Ongoing"
        
        value_inc_vat = rate["value_inc_vat"]
        
        print(f"Rate from {valid_from_bst.strftime('%Y-%m-%dT%H:%M:%S%z')} to {valid_to_str}: {value_inc_vat} p/kWh (including VAT)")
 
        # Here, we will use the asyncio's run method to execute the asynchronous function
        import asyncio
        asyncio.run(control_smart_plug(value_inc_vat))
        
if __name__ == "__main__":
    main()
