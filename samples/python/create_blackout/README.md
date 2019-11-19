# Create Blackout

## Endpoint Overview

The Create Blackout endpoint allows for the creation of a new blackout in InsightAppSec with details based upon the 
body provided in the request. This endpoint can be used for creating both app-specific and global blackouts, 
depending on whether an application is specified in the body.

## API Request

Create Blackout is a `POST` endpoint, meaning that we'll be passing a body of data in the request to create a new 
resource in InsightAppSec. In order to make the request, we'll be utilizing the standard parameters that are detailed 
in our [API Overview](../README.md). We'll also need a couple of additional items.

First, we need to import another library that we'll be using later to aid in our API request: `json`. This import 
will allow us to properly format the body we pass in the request.

```
import json
```

As just mentioned, we also need a body for the request. This body will contain information to configure the blackout 
exactly as we want it.

```
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
```

With this example payload, we're creating a blackout and providing an app ID, meaning that it will be associated with 
a single application in InsightAppSec. If we were to delete the `app` part of the body entirely, then this blackout 
would be global.

We're also supplying a name, the times for when we want it to take place, and the frequency. In this case we're 
creating a one-time blackout that applies over a span of two hours on a specific date.

Finally, we need the `api_path` for the request, and in this case it's `blackouts`.

```
api_path = "blackouts"
```

With all of our other standard parameters assigned, performing the request is simple and requires the usage of our 
imported `requests` library. In this case we make the call `requests.post` due to the endpoint type, and we pass in 
three parameters:

* `full_url` - The API base URL + the endpoint path
* `headers` - Contains our API key for authentication, and the `Content-Type` field to specify the type of data we're 
sending in the request body
* `body` - Contains our parameters for specifying blackout details

```
response = requests.post(url=full_url, headers=headers, data=json.dumps(body))
```

When assigning our `body` to the `data` parameter, notice the use of `json.dumps()`. What this is doing is converting 
our original `body` dictionary object to a JSON string. We need this parameter to be a JSON string because of the 
`Content-Type` we're supplying for the request: `application/json`. This will ensure the API can read and process the 
body of our call accordingly.

## Output

The `response` parameter will contain a status code to let us know whether the request succeeded. A successful 
request to this particular `POST` endpoint will result in a `201 Created` status code. This indicates that the API has 
successfully completed the request as we specified and resulted in a new blackout being created in InsightAppSec.

To ensure we handle any cases where the call did not succeed as expected, we can still use the following line to raise 
an HTTP error if one occurred:

```
response.raise_for_status()
```

We can also print the status code if we want to confirm that the call succeeded, and we should see a `201`.

```
print(response.status_code)
```

There's another valuable piece of data resulting from this API call that we can obtain via the `response` parameter: 
the new blackout ID. When a new blackout is created, it gets a unique identifier associated with it, and that ID can be 
used to reference it in subsequent API calls if needed.

This ID is returned in the headers of our `response`, specifically the `location` header. We can retrieve it as such:

```
blackout_url = response.headers.get("location")
```

This will return a full URL that can be used to access the newly created blackout, with the ID at the very end.

```
https://us.api.insight.rapid7.com:443/ias/v1/blackouts/00000000-0000-0000-0000-000000000001
```

If we want to obtain solely the ID for usage elsewhere, we can do that by splitting the URL string.

```
url_split = blackout_url.split("/")
blackout_id = url_split[-1]
```

This will split the URL into a list of strings with `/` acting as the separator, and then grab the last item in 
that list: the blackout ID. With that ID, we can easily reference our new blackout in subsequent API calls.

Create Blackout, along with the other blackout-related endpoints, can be utilized to simplify and/or automate the 
management of blackouts in InsightAppSec. This can be practical when coordinating large numbers of scans across 
multiple applications to ensure that blackouts are applied wherever necessary.