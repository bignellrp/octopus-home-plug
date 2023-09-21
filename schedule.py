import schedule
import time

def activate_smart_plug_job():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(activate_smart_plug("YOUR_PLUG_IP_ADDRESS"))

def activate_smart_plug_at_time(time_str):
    schedule.every().day.at(time_str).do(activate_smart_plug_job)

# Example:
activate_smart_plug_at_time("13:45")  # This will activate the plug every day at 1:45 PM.

# Keep the script running to check for scheduled tasks:
while True:
    schedule.run_pending()
    time.sleep(1)
