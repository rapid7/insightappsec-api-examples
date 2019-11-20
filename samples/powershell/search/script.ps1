# Set up URI
$region = 'us'
$api_url = "https://$region.api.insight.rapid7.com/ias/v1/"
$api_endpoint = 'search'
$uri = $api_url + $api_endpoint

# Set up headers for request
$apiKey = 'Your-api-key-here'
$headers = @{
    'X-Api-Key' = $apiKey; 'Content-Type' = 'application/json'
}

# Create body and convert to JSON
$body = @{
    'type' = 'VULNERABILITY'; 
    'query' = "vulnerability.scans.id='00000000-0000-0000-0000-000000000000'"
}
$body = $body | ConvertTo-Json

# Vulns will hold all of the returned vulnerability data
$vulns = @()

$continue = $true
Do {
    # Do POST request
    $output = Invoke-RestMethod -Uri $uri -Headers $headers -Body $body -Method 'POST'
    
    # Add vulnerabilities to our vulns list
    $vulns = $vulns + $output.data

    # If more data is left
    If ($vulns.Length -lt $output.metadata.total_data){
        # set URI for next page of data
        for ($i=0; $i -lt $output.links.Length; $i++){
            if ($output.links[$i].rel -eq 'next') {
                $uri = $output.links[$i].href
                break
            }
        }
    }
    Else {
        $continue = $false
    }

} Until ($continue -eq $false)

# Output number of apps returned
echo "Number of scan vulnerabilities returned: $($vulns.Length)"
