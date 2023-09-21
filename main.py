import requests

API_ENDPOINT = "https://api.octopus.energy/v1/products/{product_code}/electricity-tariffs/{tariff_code}/standard-unit-rates/"

def fetch_rates(product_code, tariff_code, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.get(API_ENDPOINT.format(product_code=product_code, tariff_code=tariff_code), headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

# Example
rates = fetch_rates("YOUR_PRODUCT_CODE", "YOUR_TARIFF_CODE", "YOUR_API_KEY")

def get_cheapest_rate_time(rates):
    cheapest_rate = float('inf')
    cheapest_time = None
    for rate in rates["results"]:
        if rate["value_inc_vat"] < cheapest_rate:
            cheapest_rate = rate["value_inc_vat"]
            cheapest_time = rate["valid_from"]
    return cheapest_time

# Example
cheapest_time = get_cheapest_rate_time(rates)

def activate_smart_plug_at_time(plug, time):
    # This function will vary based on the smart plug's API or SDK
    pass

def main():
    rates = fetch_rates("YOUR_PRODUCT_CODE", "YOUR_TARIFF_CODE", "YOUR_API_KEY")
    cheapest_time = get_cheapest_rate_time(rates)
    activate_smart_plug_at_time("YOUR_SMART_PLUG_IDENTIFIER", cheapest_time)

if __name__ == "__main__":
    main()
