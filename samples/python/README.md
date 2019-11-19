# API Overview

Throughout each of our InsightAppSec API examples, there are a few concepts that are consistently applicable, regardless 
of the endpoint or the data associated with it. These include:

1. Imports
2. Parameters
3. Response
4. Pagination

We'll walk through each of these sections in detail to provide a better understanding of them and how they will apply 
across all of our InsightAppSec API examples. This will also aid in ensuring we adhere to API best practices.

## Imports

First we can address imports, or the notion of gaining access to code in another module so we can utilize it in our 
script. We'll need a single import to be able to complete an API request, and in this case it's the `requests` library. 
This is the standard library used in Python for making HTTP requests.

At the very top of the script we can add the following line to perform this import.

```
import requests
```

The `requests` library abstracts complex API logic and allows us to easily perform API interactions by directly making 
calls in accordance with our desired action, such as `requests.get()`.

## Parameters

There are a few parameters that will be consistently required across all InsightAppSec API requests. First is the URL, 
which states which endpoint we'll be accessing when making an API call. The base API URL in InsightAppSec can be set 
as the following:

```
region = "us"
api_url = f"https://{region}.api.insight.rapid7.com/ias/v1/"
```

Note the usage of the `region` parameter. This refers to your InsightAppSec region and will dictate the base URL used 
for making API calls. In this case we are formatting the base URL to account for this region, and it will read as 
`https://us.api.insight.rapid7.com/ias/v1/`.

If you're uncertain of your region, a complete listing of them is available [here](https://insight.help.rapid7.com/docs/product-apis#section-supported-regions).

Another component of the API URL is the path, which refers to the specific endpoint being referenced in the API call. 
This will vary between endpoints, with some even containing URL parameters. The path can be set and then combined with 
the `api_url` to form a complete API URL that we'll use in making our request.

```
api_path = "path"
full_url = api_url + api_path
```

Another parameter that will always be required is the InsightAppSec API key. This key is used in authenticating to the
Rapid7 InsightAppSec API and is a necessity for every single API call. It can be set as a string parameter and will 
later be used when performing a request. Rapid7 recommends the encryption and secure storage of sensitive values such 
as this one to ensure best security practices, but we have it displayed in this manner for readability purposes.

```
api_key = "Your-API-key-here"
```

The last API request-related parameter that must be defined is the `header`. Headers can be used to pass additional 
information that's needed to make an API request. In this case we need to pass our InsightAppSec API key as a header 
called `X-Api-Key` to perform authentication.

Another `header` we'll need in some instances is `Content-Type`, which is used in `POST` or `PUT` requests to indicate 
the type of data being sent. For InsightAppSec API requests, it's best to use the `application/json` content type.

With these headers in mind, we can create a dictionary (which is a set of key-value pairs) that will hold values for 
both the `X-Api-Key` and `Content-Type` fields.

```
headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}
``` 

To summarize, the fields required for performing an API request are the API URL (consisting of the base URL and the 
path), the InsightAppSec API key, and the content type.

```
api_url = "https://us.api.insight.rapid7.com/ias/v1/"
api_path = "path"
full_url = api_url + api_path
api_key = "Your-API-key-here"
headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}
```

## Response

A Response object is returned when completing a Python API request. This object will contain a lot of information about 
the API request we performed, including a status code that informs us of the success of the call, as well as any 
data retrieved. It's ideal to have logic in place to handle any errors (aka exceptions) that may occur during the call, 
as we would not want to proceed with trying to utilize data retrieved from the API call if it was unsuccessful.

To do this, it's best to use `try` and `except` blocks that encompass the API logic and perform handling for exceptions 
that may arise. There are several different types of exceptions available in the `requests` library that can be used in 
this handling.

```
try:
    response = requests.get(full_url, headers=headers)
    response.raise_for_status()
except requests.exceptions.HTTPError as he:
    print("HTTP error: ", he)
except requests.exceptions.ConnectionError as ce:
    print("Connection error: ", ce)
except requests.exceptions.RequestException as e:
    print("Request exception: ", e)
```

The line `response.raise_for_status()` is important here, as it will raise an HTTP error if one occurred. The error 
should print with a status code, which provides more detail about why the API call failed. The other exceptions are of 
different types, with `RequestException` being the most generic of those given.

If no exception occurs, then we can safely proceed to utilize data retrieved (if any) from the API call. We can obtain 
this data from the `response` parameter, which you can see above is set to receive the response from our API call. 
There are a couple ways to extract data from the `response` parameter.

If you'd prefer the output to be a plain string containing all of the data retrieved, then you can obtain this via 
`response.text`. If you'd prefer to have a dictionary - a mapping of key-value pairs - then you can use 
`response.json()`.

```
response_text = response.text
response_dict = response.json()
```

With your data in hand, you can then proceed to use it as desired.

## Pagination

In many `GET` requests made to the InsightAppSec API (and some `POST` requests), there is something known as pagination.
Pagination is used to limit the return of data sets to a reasonable size or amount. With many APIs, including the Rapid7
InsightAppSec API, there is a lot of data at play and thus there exists the potential to return massive amounts of it. 
Retrieving all of that in a single call is not ideal, and so pagination is used to alleviate this issue.

In API requests where there is the potential to pull back multiple pieces of data, the API provides additional 
information about how much total data exists and how we can retrieve it.

```
"metadata": {
    "index": 0,
    "size": 50,
    "total_data": 806,
    "total_pages": 17
  },
  "links": [
    {
      "rel": "first",
      "href": "https://us.api.insight.rapid7.com:443/ias/v1/search?index=0&size=50"
    },
    {
      "rel": "self",
      "href": "https://us.api.insight.rapid7.com:443/ias/v1/search"
    },
    {
      "rel": "next",
      "href": "https://us.api.insight.rapid7.com:443/ias/v1/search?index=1&size=50"
    },
    {
      "rel": "last",
      "href": "https://us.api.insight.rapid7.com:443/ias/v1/search?index=16&size=50"
    }
  ]
```

The `total_data` field in the `metadata` section is telling us that there are 806 total results in this API call, with 
50 of them having been retrieved so far. Additionally, there is the `next` URL under the `links` section. This is the 
URL that we can use to make another API call and retrieve the next "page" of results. Utilizing that URL will give us 
50 more results, after which we want to use the new `next` URL to retrieve the next page of results. This cycle will 
continue until we've retrieved all 806 results.

To employ this logic in the code, it's best to use a while loop to continue iterating over each page until we've reached
the final one.

```
data = []
cont = True

while cont:
    response = requests.get(full_url, headers=headers)

    response_dict = response.json()

    data.extend(response_dict.get("data"))

    if len(data) >= response_dict.get("metadata").get("total_data"):
        cont = False
    else:
        for x in response_dict.get("links"):
            if x.get("rel") == "next":
                full_url = x.get("href")
                break
```

This logic begins with an empty list called `data`, which is where we will add all the data we retrieve in each round 
of our API calls, and `cont`, which is a boolean that will tell us whether to continue in our loop. After that, we enter
the loop and perform the following steps:

  1. Make API request
  2. Add the data we've received to the `data` list, which will hold all of our data
  3. Check if there's more data to retrieve by comparing `total_data` to the length of our `data` list
     - If so, get our new API URL called `next` from the `links` property in our `response` and continue in the loop
     - If not, end the while loop, as there is no more data for us to retrieve
     
This simple method will result in the retrieval of all data from the specified endpoint, regardless of how much or the 
number of pages.

## Conclusion

With each of these concepts being applicable across the InsightAppSec API, we now have a solid foundation for delving 
into individual endpoints and further understanding their usage. Read on to check out the walkthroughs we've created 
for some specific InsightAppSec API endpoints.