import requests

# Setup standard parameters
region = "us"
api_url = f"https://{region}.api.insight.rapid7.com/ias/v1/"
api_key = "Your-api-key-here"
api_path = "schedules/"
schedule_id = "00000000-0000-0000-0000-000000000000"
full_url = api_url + api_path + schedule_id

headers = {"X-Api-Key": api_key}

try:
    # Make API request
    response = requests.delete(url=full_url, headers=headers)

    # Raise HTTP Error if it occurred
    response.raise_for_status()

    # Print status code
    print(response.status_code)
except requests.exceptions.HTTPError as he:
    print("HTTP error:", he)
except requests.exceptions.ConnectionError as ce:
    print("Connection error:", ce)
except requests.exceptions.RequestException as e:
    print("Request exception:", e)
