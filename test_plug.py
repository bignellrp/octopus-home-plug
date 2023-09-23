import os
from dotenv import load_dotenv
from PyP100 import PyP100

# Load values from .env
load_dotenv()

# Access the API key
EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]
SMART_PLUG_IP = os.environ["SMART_PLUG_IP"]

def control_smart_plug(action):
    plug = PyP100.P100(SMART_PLUG_IP, EMAIL, PASSWORD)

    plug.handshake() #Creates the cookies required for further methods
    plug.login() #Sends credentials to the plug and creates AES Key and IV for further methods

    if action == "on":
        plug.turnOn()
        print("Turned on the smart plug due to low rate.")
    elif action == "off":
        plug.turnOff()
        print("Turned off the smart plug due to high rate.")

control_smart_plug("on")