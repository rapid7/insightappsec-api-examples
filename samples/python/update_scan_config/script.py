import requests
import json

# Setup standard parameters
region = "us"
api_url = f"https://{region}.api.insight.rapid7.com/ias/v1/"
api_key = "Your-api-key-here"
api_path = "scan-configs/"
scan_config_id = "00000000-0000-0000-0000-000000000000"
full_url = api_url + api_path + scan_config_id

headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}

body = {
    "name": "Scan Config",
    "description": "Scan config description",
    "app": {
        "id": "00000000-0000-0000-0000-000000000001"
    },
    "attack_template": {
        "id": "00000000-0000-0000-0000-000000000002"
    },
    "assignment": {
        "type": "ENGINE_GROUP",
        "environment": "CLOUD"
    }
}

try:
    # Make API request
    response = requests.put(url=full_url, headers=headers, data=json.dumps(body))

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
