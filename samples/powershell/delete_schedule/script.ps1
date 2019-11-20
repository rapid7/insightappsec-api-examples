# Set up URI
$region = 'us'
$api_url = "https://$region.api.insight.rapid7.com/ias/v1/"
$api_endpoint = 'schedules/'
$schedule_id = '00000000-0000-0000-0000-000000000000'
$uri = $api_url + $api_endpoint + $schedule_id

# Set up headers for request
$apiKey = 'Your-api-key-here'
$headers = @{'X-Api-Key' = $apiKey}

# Do DELETE request
$output = Invoke-WebRequest -Uri $uri -Headers $headers -Body $body -Method 'DELETE'

# Print status code of response
echo $output.StatusCode
