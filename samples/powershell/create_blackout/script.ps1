# Set up URI
$region = 'us'
$api_url = "https://$region.api.insight.rapid7.com/ias/v1/"
$api_endpoint = 'blackouts'
$uri = $api_url + $api_endpoint

# Set up headers for request
$apiKey = 'your-api-key-here'
$headers = @{
    'X-Api-Key' = $apiKey; 'Content-Type' = 'application/json'
}

# Create body and convert to JSON
$body = @{
    "name" = "Blackout";
    "enabled" = "true";
    "app" = @{
        "id" = "00000000-0000-0000-0000-000000000000"
    };
    "first_start" = "2019-10-15T21:00:00Z";
    "first_end" = "2019-10-15T23:00:00Z";
    "frequency" = @{
        "type" = "ONCE";
        "interval" = 0
    }
}
$body = $body | ConvertTo-Json

# Do POST request
$output = Invoke-WebRequest -Uri $uri -Headers $headers -Body $body -Method 'POST'

# Get the new blackout ID
$blackout_url = $output.Headers["Location"]
$url_split = $blackout_url.split("/")
$blackout_id = $url_split[$url_split.Count - 1]

# Print blackout ID
echo $blackout_id
