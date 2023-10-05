import os
from dotenv import load_dotenv
from fordpass import Vehicle
import asyncio
import requests

# Load values from .env
load_dotenv()

async def main():
    FORD_USERNAME = os.environ["FORD_USERNAME"]
    FORD_PASSWORD = os.environ["FORD_PASSWORD"]
    VIN = os.environ["VIN"]

    # Initialize the vehicle object.
    vehicle = Vehicle(FORD_USERNAME, FORD_PASSWORD, VIN)

    # Log in
    try:
        ...
        await vehicle.auth()
        ...
    except requests.exceptions.HTTPError as e:
        print(f"An HTTP error occurred: {e}")
        # Here, print out the response body for better debugging.
        print(e.response.text)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Get vehicle status.
    status = await vehicle.status()
    
    # Extract and print the charging status.
    charging_status = status["batteryFillLevel"]
    print(f"Charging Status: {charging_status}%")

# Run the async function
asyncio.run(main())