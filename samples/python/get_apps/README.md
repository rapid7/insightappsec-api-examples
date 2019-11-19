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

If you'll recall from the API Overview, we need to set an `api_path` parameter in order to make the call to this 
particular endpoint. In this case, our `api_path` parameter will be `apps`.

```
api_path = "apps"
``` 

With all of our other standard parameters assigned, performing the request is simple and requires the usage of our 
imported `requests` library. In this case we make the call `requests.get` due to the endpoint type, and we pass in two 
parameters:

* `full_url` - The API base URL + the endpoint path
* `headers` - Contains our API key for authentication

The `Content-Type` header is not necessary here since we're not sending a body of data along with the request.

```
response = requests.get(url=full_url, headers=headers)
```

Here we can see a `response` parameter that will be receiving the response from the API call.

## Output

Once we've done our simple `requests.get` and have a successful API call, we can retrieve the desired application 
information from our `response` parameter.

```
response_dict = response.json()
```

Now we have our `response_dict`, which is a dictionary or mapping of key-value pairs, that holds all of the 
information retrieved in the call to Get Apps. Though this will contain multiple types of information (such as 
`metadata` and `links`), the application data we're looking for will exist under the `data` field in our 
`response_dict`.

```
app_data = response_dict.get("data")
```

The `data` field contains a list of applications.

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

Now that we have our application data, we can proceed to utilize it in any way we'd like. This includes making 
subsequent API calls to retrieve more application-related information, such as scans, vulnerabilities, and more.