# Delete Schedule

## Endpoint Overview

The Delete Schedule endpoint is straightforward in that it deletes a single scanning schedule from InsightAppSec, based 
on the schedule ID that is provided. This means that the schedule will no longer be available for use in InsightAppSec. 
This can help further ease the process of schedule management, particularly when juggling a larger number of 
applications.

It's important to be cautious when utilizing any `DELETE` endpoints like this one, as they can delete data in a 
permanent manner such that it is no longer accessible or retrievable.

## API Request

Delete Schedule is a `DELETE` endpoint, meaning that we'll be erasing data from InsightAppSec in the event of a 
successful API call. In order to make the request, we'll be utilizing the standard parameters that are detailed in our 
[API Overview](../README.md).

There is an additional parameter we'll need here, as well. In order to tell the API which schedule we want to delete, 
we need to provide a schedule ID. This ID will become a URL parameter - a string that is appended to the end of our  
endpoint URL so we can successfully complete the call.

Let's ensure we have this URL correctly formatted. First, we need our `api_endpoint`, which in this case is just 
`schedules`.

```
$api_endpoint = 'schedules/'
```

Note the `/` at the end of that path. It's there because we need to add the schedule ID afterwards. We can set our 
schedule ID as a separate variable like so:

```
$schedule_id = '00000000-0000-0000-0000-000000000000'
```

Finally, we want to combine the base URL, the API path, and this schedule ID URL parameter to construct our full URL.

```
$uri = $api_url + $api_endpoint + $schedule_id
```

By concatenating all of those values together, we should have a URL that resembles the following:

```
https://us.api.insight.rapid7.com/ias/v1/schedules/00000000-0000-0000-0000-000000000000
```

With all of our other standard parameters assigned, performing the request is simple and requires the usage of the `Invoke-WebRequest` function. 

```
$output = Invoke-WebRequest -Uri $uri -Headers $headers -Body $body -Method 'DELETE'
```

You may notice that we used `Invoke-WebRequest` rather than `Invoke-RestMethod` which we frequently use in other examples.
The reason for this is that we want to be able to access the status code of the response to our request, and `Invoke-WebRequest`
allows us to do so.

## Output

Although we are using a `$output` variable to retrieve the response from the API call, we're not actually receiving 
any data here. Rather, we're performing a single action and want to ensure that it was successful.

The status code on the `$output` object will provide this information. A successful request to this particular 
`DELETE` endpoint will result in a `204 No Content` status code. This indicates that the API has successfully completed 
the request as we specified and that there is no content to send in the response body.

We can print the status code if we want to confirm that the call succeeded, and we should see a `204`.

```
echo $output.StatusCode
```

With the schedule deleted, we can proceed to utilize other schedule-related endpoints to create and update them as 
desired. This can help simplify schedule management for larger numbers of applications and further ease the application 
onboarding process.