import requests
import json

# Setup standard parameters
region = "us"
api_url = f"https://{region}.api.insight.rapid7.com/ias/v1/"
api_key = "Your-api-key-here"
api_path = "blackouts"
full_url = api_url + api_path

headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}

body = {
    "name": "Blackout",
    "enabled": "true",
    "app": {
        "id": "00000000-0000-0000-0000-000000000000"
    },
    "first_start": "2019-10-15T21:00:00Z",
    "first_end": "2019-10-15T23:00:00Z",
    "frequency": {
        "type": "ONCE",
        "interval": 0
    }
}

try:
    # Make API request
    response = requests.post(url=full_url, headers=headers, data=json.dumps(body))

    # Raise HTTP Error if it occurred
    response.raise_for_status()

    # Print status code
    print(response.status_code)

    # Get the new blackout ID
    blackout_url = response.headers.get("location")
    url_split = blackout_url.split("/")
    blackout_id = url_split[-1]

    # Print blackout ID
    print(blackout_id)
except requests.exceptions.HTTPError as he:
    print("HTTP error:", he)
except requests.exceptions.ConnectionError as ce:
    print("Connection error:", ce)
except requests.exceptions.RequestException as e:
    print("Request exception:", e)
