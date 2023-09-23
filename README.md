# octopus-home-plug
A python app for controlling the smart plug based on the cheapest Octopus rates

Controlling a smart plug based on electricity rates from the Octopus Energy API is a multi-step process. The basic steps are:

Fetch Electricity Rates from Octopus Energy API.
Determine the Cheapest Rate.
Control the Smart Plug based on the cheapest rate.

Below is a generalised guide. I'll use Python for the API fetching and logic, but the method to control your smart plug will depend on its brand and whether it has an available API or SDK.

# 1. Fetch Electricity Rates
First, you'll need to set up an API key with Octopus Energy and fetch the electricity rates.

https://octopus.com/docs/octopus-rest-api/how-to-create-an-api-key

# 2. Determine the Cheapest Rate
Once you have the rates, you can analyse them to determine when the cheapest rate occurs. This required parsing the times and rates and finding the lowest value.

# 3. Control the Smart Plug
The method to control your smart plug will depend on the brand and model. Some smart plugs come with APIs or SDKs that let you control them programmatically. For example, if you're using a TP-Link smart plug, there's a Python library called PyP100 that can help you control it. For other brands, you might need to refer to their documentation or see if there's a third-party solution available.

test_plug.py can be used to test the plug is working before setting the main.py to run on a schedule.

# 4. Putting It All Together:
With all the functions set up, you can fetch the rates daily, determine the cheapest rate, and then set your smart plug to activate at that time. One way to do this is to build a container with github actions and run the main.py on a cron every 30 minutes.

This is a very basic and generalised overview. Depending on your requirements, you might need to add additional error handling, logging, web frontend, more specific time parsing, and other refinements.

# Optional. Discord alerts

If you have a Discord server you can create a webhook and update a channel when the plug is activated.