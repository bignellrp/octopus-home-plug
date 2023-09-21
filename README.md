# octopus-home-plug
A python app for controlling the SmartLife plug based on the cheapest Octopus rates

Controlling a smart plug based on electricity rates from the Octopus Energy API is a multi-step process. The basic steps are:

Fetch Electricity Rates from Octopus Energy API.
Determine the Cheapest Rate.
Control the Smart Plug based on the cheapest rate.

Below is a generalized guide. I'll use Python for the API fetching and logic, but the method to control your smart plug will depend on its brand and whether it has an available API or SDK.

# 1. Fetch Electricity Rates
First, you'll need to set up an API key with Octopus Energy and fetch the electricity rates.

# 2. Determine the Cheapest Rate
Once you have the rates, you can analyze them to determine when the cheapest rate occurs. This might require parsing the times and rates and finding the lowest value.

# 3. Control the Smart Plug
The method to control your smart plug will depend on the brand and model. Some smart plugs come with APIs or SDKs that let you control them programmatically. For example, if you're using a TP-Link smart plug, there's a Python library called pyHS100 that can help you control it. For other brands, you might need to refer to their documentation or see if there's a third-party solution available.

# 4. Putting It All Together:
With all the functions set up, you can fetch the rates daily, determine the cheapest rate, and then set your smart plug to activate at that time.

This is a very basic and generalized overview. Depending on your requirements, you might need to add error handling, logging, more specific time parsing, and other refinements.
