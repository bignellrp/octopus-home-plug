import requests
import os
from dotenv import load_dotenv

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

def main():
    rates_data = fetch_rates()
    
    # Assuming the rates are in the "results" key, based on the typical structure of Octopus Energy API responses:
    for rate in rates_data["results"]:
        valid_from = rate["valid_from"]
        valid_to = rate.get("valid_to", "Ongoing")  # Some rates might not have a "valid_to" timestamp
        value_inc_vat = rate["value_inc_vat"]
        
        print(f"Rate from {valid_from} to {valid_to}: {value_inc_vat} p/kWh (including VAT)")

if __name__ == "__main__":
    main()
