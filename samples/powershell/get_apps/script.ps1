$region = 'us'
$baseUrl = "https://$region.api.insight.rapid7.com/ias/v1/"
$apiKey = 'Your-api-key-here'
$headers = @{
    'X-Api-Key' = $apiKey
}

# Apps will hold all the returned applications
$apps = @()

$uri = $baseUrl + 'apps' + '?index=0&size=5&sort=app.name,ASC'
$continue = $true
Do {
    $output = Invoke-RestMethod -Uri $uri -Headers $headers -Method 'GET'

    # Retrieve data from response 
    $appData = $output.data

    # Add apps to our apps list
    $apps = $apps + $appData

    # Get next reference
    $next = $false
    for ($i=0; $i -lt $output.links.Length; $i++){
        if ($output.links[$i].rel -eq 'next') {
            $uri = $output.links[$i].href
            $next = $true
            break
        }
    }

    # Don't continue paging
    if (!$next){
        $continue = $false
    }
} Until ($continue -eq $false)

# Output number of apps returned
Write-Output "Number of apps returned: $($apps.Length)"
