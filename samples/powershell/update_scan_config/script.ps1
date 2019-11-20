# Setup standard parameters
$region = 'us'
$api_url = "https://$region.api.insight.rapid7.com/ias/v1/"
$api_endpoint = 'scan-configs/'
$scan_config_id = '00000000-0000-0000-0000-000000000000'
$uri = $api_url + $api_endpoint + $scan_config_id

# Set up headers
$api_key = "Your-api-key-here"
$headers = @{"X-Api-Key": $api_key, "Content-Type": 'application/json'}

# Body to send to endpoint
$body = @{
    'name' = 'Scan Config';
    'description' = 'Scan config description';
    'app' = @{
        "id": '00000000-0000-0000-0000-000000000001'
    };
    "attack_template" = @{
        'id' = '00000000-0000-0000-0000-000000000002'
    };
    "assignment" = @{
        'type' = 'ENGINE_GROUP';
        'environment' = 'CLOUD'
    }
}
$body = $body | ConvertTo-Json

# Make PUT request
$output = Invoke-WebRequest -Uri $uri -Headers $headers -Body $body -Method 'PUT'

# Print status code (expecting 200)
echo $output.StatusCode
