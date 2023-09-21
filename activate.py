from kasa import SmartPlug
import asyncio

async def activate_smart_plug(ip_address):
    plug = SmartPlug(ip_address)
    
    # Update the device state:
    await plug.update()

    # Print basic device info:
    print(f"Device at {ip_address} is {plug.alias} model of type {plug.device_type}.")
    
    # Turn on the plug:
    await plug.turn_on()

# To run the asynchronous function:
loop = asyncio.get_event_loop()
loop.run_until_complete(activate_smart_plug("YOUR_PLUG_IP_ADDRESS"))
