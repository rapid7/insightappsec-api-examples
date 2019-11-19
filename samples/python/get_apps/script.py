import requests

# Setup standard parameters
region = "us"
api_url = f"https://{region}.api.insight.rapid7.com/ias/v1/"
api_key = "Your-api-key-here"
api_path = "apps"
full_url = api_url + api_path

headers = {"X-Api-Key": api_key}

apps = []
cont = True

try:
    while cont:
        # Make API request
        response = requests.get(url=full_url, headers=headers)

        # Raise HTTP Error if it occurred
        response.raise_for_status()

        # Get data from response object
        response_dict = response.json()

        # Add app data to our apps list
        apps.extend(response_dict.get("data"))

        # If the length of apps >= total_data, then there's no more data to retrieve
        if len(apps) >= response_dict.get("metadata").get("total_data"):
            cont = False
        else:
            # Loop through the list of links
            for x in response_dict.get("links"):
                # If it's the 'next' link, store it in full_url and continue loop
                if x.get("rel") == "next":
                    full_url = x.get("href")
                    break
except requests.exceptions.HTTPError as he:
    print("HTTP error:", he)
except requests.exceptions.ConnectionError as ce:
    print("Connection error:", ce)
except requests.exceptions.RequestException as e:
    print("Request exception:", e)
