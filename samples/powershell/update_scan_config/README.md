# Update Scan Config

## Endpoint Overview

The Update Scan Config endpoint allows updates to be made to an existing scan configuration in InsightAppSec, based 
on the body provided in the request. This endpoint presents options for altering basic details within the scan config, 
including things like attack template and engine assignment.

## API Request

Update Scan Config is a `PUT` endpoint, meaning that we'll be passing a body of data in the request to make updates 
to an existing entity in InsightAppSec. In order to make the request, we'll be utilizing the standard parameters that 
are detailed in our [API Overview](../README.md). We'll also need a couple of additional items.

Firstly, we need our `api_endpoint`, as well as another URL parameter that's necessary for specifying which scan config we 
want to update. In this case, our `api_endpoint` is `scan-configs`.

```
$api_endpoint = 'scan-configs/'
``` 

Note the `/` at the end of that path. It's there because we need to add the scan config ID afterwards. We can set our 
scan config ID as a separate variable like so:

```
$scan_config_id = '00000000-0000-0000-0000-000000000000'
```

Finally, we want to combine the base URL, the API path, and this scan config ID URL parameter to construct our full URL.

```
$uri = $api_url + $api_endpoint + $scan_config_id
```

By concatenating all of those values together, we should have a URL that resembles the following:

```
https://us.api.insight.rapid7.com/ias/v1/scan-configs/00000000-0000-0000-0000-000000000000
```

Finally, we need a body for the request. This body will contain information to indicate the fields and values that 
we want to update for our scan configuration.

```
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
```

Note the use of `ConvertTo-Json` to transform our request body into JSON format which the endpoint requires.

With this example payload, we're supplying the attack template used during application scans, as well as the engine 
group assignment. This will result in updates to fundamental elements that are utilized in every scan.

With our full URL constructed, we can move on to the API request itself. Performing the request is simple and requires 
the usage of `Invoke-WebRequest` with the following parameters

* `uri` - The API base URL + the endpoint path + the scan config ID
* `headers` - Contains our API key for authentication, and the `Content-Type` field to specify the type of data we're 
sending in the request body
* `body` - Contains our parameters for updating the scan configuration

```
$output = Invoke-WebRequest -Uri $uri -Headers $headers -Body $body -Method 'PUT'
```

Note the use of `ConvertTo-Json` to transform our request body into a JSON-formatted string.
We need this parameter to be a JSON string because of the `Content-Type` we're supplying for the request:
`application/json`. This will ensure the API can read and process the
body of our call accordingly.

## Output

Although we are using a `$output` parameter to retrieve the response from the API call, we're not actually receiving 
any data here. Rather, we're performing an update on an existing entity in InsightAppSec and want to ensure that it 
was successful.

The status code on the `$output` object will provide this information. A successful request to this particular `PUT` 
endpoint will result in a `200` status code. This indicates that the API has successfully completed the request as we 
specified and that the scan config was updated appropriately.

We can print the status code if we want to confirm that the call succeeded, and we should see a `200`.

```
echo $output.StatusCode
```

Update Scan Config, along with its fellow scan config-related endpoints, can be utilized to dynamically maintain 
configurations used in application scanning. This can aid tremendously in the application onboarding process by 
enabling the automation of scan configuration management, and simplify maintenance by providing an array of 
options for customization.