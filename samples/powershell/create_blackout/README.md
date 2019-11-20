# Create Blackout

## Endpoint Overview

The Create Blackout endpoint allows for the creation of a new blackout in InsightAppSec with details based upon the 
body provided in the request. This endpoint can be used for creating both app-specific and global blackouts, 
depending on whether an application is specified in the body.

## API Request

Create Blackout is a `POST` endpoint, meaning that we'll be passing a body of data in the request to create a new 
resource in InsightAppSec. In order to make the request, we'll be utilizing the standard parameters that are detailed 
in our [API Overview](../README.md). We'll also need a couple of additional items.

Here's an example body that we can use in this API call:

```
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
```

With this example payload, we're creating a blackout and providing an app ID, meaning that it will be associated with 
a single application in InsightAppSec. If we were to delete the `app` part of the body entirely, then this blackout 
would be global.

We're also supplying a name, the times for when we want it to take place, and the frequency. In this case we're 
creating a one-time blackout that applies over a span of two hours on a specific date.

Finally, we need the `api_endpoint` for the request, and in this case it's `blackouts`.

```
api_endpoint = "blackouts"
```

With all of our other standard parameters assigned, performing the request is simple and requires the usage of the `Invoke-WebRequest` function. 

```
$output = Invoke-WebRequest -Uri $uri -Headers $headers -Body $body -Method 'POST'
```

You may notice that we used `Invoke-WebRequest` rather than `Invoke-RestMethod` which we frequently use in other examples.
The reason for this is that we want to be able to access the headers of the response to our request, and `Invoke-WebRequest`
allows us to do so.

## Output
A valuable piece of data resulting from this API call that we can obtain via the `output` parameter is
the new blackout ID. When a new blackout is created, it gets a unique identifier associated with it, and that ID can be 
used to reference it in subsequent API calls if needed.

This ID is returned in the headers of our `output`, specifically the `Location` header. We can retrieve it as such:

```
$blackout_url = $output.Headers["Location"]
```

This will return a full URL that can be used to access the newly created blackout, with the ID at the very end.

```
https://us.api.insight.rapid7.com:443/ias/v1/blackouts/00000000-0000-0000-0000-000000000001
```

If we want to obtain solely the ID for usage elsewhere, we can do that by splitting the URL string.

```
$url_split = $blackout_url.split("/")
$blackout_id = $url_split[$url_split.Count - 1]
```

This will split the URL into a list of strings with `/` acting as the separator, and then grab the last item in 
that list: the blackout ID. With that ID, we can easily reference our new blackout in subsequent API calls.

Create Blackout, along with the other blackout-related endpoints, can be utilized to simplify and/or automate the 
management of blackouts in InsightAppSec. This can be practical when coordinating large numbers of scans across 
multiple applications to ensure that blackouts are applied wherever necessary.