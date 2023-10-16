# TastyIgniter Python API

This python package is an async wrapper to access the TastyIgniter order system APIs.

When initialized the API requires you to provide username and password for authentication to the TastyIgniter system as configured in the API settings. You will also need to pass the domain for the TastyIgniter instance.

The following functions are currently available:

get_locations:
Retrieve a list of restaurant locations which are configured on the system.

get_enabled_locations:
Return only locations which are currently enabled on the system.

get_orders:
Return all orders from the system.

get_received_orders:
Return only orders in Received status from the system.
