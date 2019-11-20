# Get Apps

## Endpoint Overview
The Get Apps endpoint returns a list of all applications in your instance of InsightAppSec. By default they are sorted 
by application name in ascending order.

The data returned from the Get Apps endpoint includes basic application data like the ID, name, and description. This 
data, particularly the ID, can be useful if you wish to retrieve other application-related information via the API, due 
to the fact that the application ID will almost always be required in order to complete such calls.

## API Request

Get Apps, as its name implies, is a `GET` request, meaning that we'll be retrieving information via the API when we 
make the call. In order to make the request, we'll be utilizing the standard parameters that are detailed in our 
[API Overview](../README.md).

Just like in the API overview, we should set our `$baseUrl`, `$apiKey`, and `$headers`.

```
$baseUrl = 'https://us.api.insight.rapid7.com/ias/v1/'
$apiKey = 'Your-api-key-here'
$headers = @{'X-Api-Key': $apiKey}
```

Since this is a `GET` request, the `'Content-Type': 'application/json'` field in the headers is not needed.

Next, we should create the `@params` dictionary.

```
@params = @{
Uri = $baseUrl + 'apps' + ?q=index=0,size=50,sort=app.name,ASC
Headers = $headers
Method = 'GET'
```

The `Uri` in this example is the `$baseUrl` + the applications endpoint `apps` + optional URL parameters.
The three keys shown are the parameters allowed for the Get Apps API request. The values shown are the default values.
This means that if you choose to not input URL parameters, these values will be used by default.

Finally, we can run the request.

```
$output = Invoke-RestMethod @params
``` 

# Output
Once we've run our simple `Invoke-RestMethod` cmdlet and have a successful API call, we can retrieve the desired 
application information from our `$output` variable.

The response returned by the Get Apps API call will be automatically mapped to a dictionary by the `Invoke-RestMethod` 
cmdlet. The response will contain three sub dictionaries: `data`, `metadata`, and `links`. The information on specific 
apps will be in the `data` sub dictionaries:

```
$appData = $output.data
```

This line will create a new variable called `$appData` that will store only the information in the data sub dictionary.
`$appData` will be a list of apps, each represented by data in dictionary form.

```
"data": [
    {
      "id": "00000000-0000-0000-0000-000000000000",
      "name": "My Application",
      "description": "My Application Description",
      "links": [
        {
          "rel": "self",
          "href": "https://us.api.insight.rapid7.com:443/ias/v1/apps/00000000-0000-0000-0000-000000000000"
        }
      ]
    },
    {
      "id": "00000000-0000-0000-0000-000000000001",
      "name": "My Next Application",
      "description": "My Next Application Description",
      "links": [
        {
          "rel": "self",
          "href": "https://us.api.insight.rapid7.com:443/ias/v1/apps/00000000-0000-0000-0000-000000000001"
        }
      ]
    }
  ]
```

Each app contains the fields app ID, name, description, and links. Specific information can be accessed as such:

```
$elementId = $appData[0].id
```

This line would set the `elementId` variable to the ID of the first app (e.g. "00000000-0000-0000-0000-000000000000").

Another useful way to manipulate the output would be finding a specific app ID when you know the name of the app.
Say we want to find the App ID of `My Next Application`.

```
for ($i=0; $i -lt $appData.Length; $i++){
    if ($appData[$i].name -eq 'My Next Application') {
        $appId = $appData[$i].id
    }
}
```

This code will set the `$appId` variable to the ID for `My Next Application` (e.g. 00000000-0000-0000-0000-000000000001).

Now that we have our application data, we can proceed to utilize it in any way we'd like. This includes making 
subsequent API calls to retrieve more application-related information, such as scans, vulnerabilities, and more.