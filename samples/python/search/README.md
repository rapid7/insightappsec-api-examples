# Search

## Endpoint Overview

The Search endpoint is incredibly flexible and perhaps one of the most powerful endpoints within the InsightAppSec API. 
It can be used to filter and retrieve a variety of information based on a user-provided query.

While additional endpoints do exist in the InsightAppSec API for retrieving specific data (say, a particular scan), 
Search broadens your capabilities by allowing the retrieval of data across different InsightAppSec components. For 
instance, searching vulnerabilities based on a particular scan ID, or searching completed scans based on a given date 
range. This usage of queries makes it easy to obtain the exact type of data you're looking for.

## API Request

The Search endpoint contains a couple of unique components that we'll review here. First, we need to import an 
additional library that we'll be using later to aid in our API request: `json`.

```
import json
```

We'll further detail the usage of this library later on when we perform the request itself.

Although Search is an endpoint used to retrieve data, it is a `POST` request. This means that, in addition to utilizing 
the standard parameters that are detailed in our [API Overview](../README.md), we will also need to provide a body for 
the request. The body we provide will contain two things: the type of data we want, and the query that will filter that 
data.

Here's an example body that we can use in this API call:

```
body = {
         "type": "VULNERABILITY",
         "query": "vulnerability.scans.id='00000000-0000-0000-0000-000000000000'"
       }
```

This body will tell the API to retrieve all vulnerabilities from the given scan ID. This is a useful reporting-type 
query for obtaining a scan's vulnerabilities without actually accessing InsightAppSec via the UI. Note the single quotes 
around the `vulnerability.scans.id` value provided, as these are required for proper query formatting.

Also note that this is just one possibility of many for search queries. Check out the [Search Catalog](https://help.rapid7.com/insightappsec/en-us/api/v1/docs.html#tag/Search)
along with the accompanying operators and examples to view a complete listing of query options.

We also need to specify our `api_path` parameter to have a complete URL for the API call, and in the case of this 
endpoint, it's `search`.

```
api_path = "search"
```

With all of our other standard parameters assigned, performing the request is simple and requires the usage of our 
imported `requests` library. In this case we make the call `requests.post` due to the endpoint type, and we pass in 
three parameters:

* `full_url` - The API base URL + the endpoint path
* `headers` - Contains our API key for authentication, and the `Content-Type` field to specify the type of data we're 
sending in the request body
* `body` - Contains our search parameters: resource type and query

```
response = requests.post(url=full_url, headers=headers, data=json.dumps(body))
```

When assigning our `body` to the `data` parameter, notice the use of `json.dumps()`. What this is doing is converting 
our original `body` dictionary object to a JSON string. We need this parameter to be a JSON string because of the 
`Content-Type` we're supplying for the request: `application/json`. This will ensure the API can read and process the 
body of our call accordingly.

## Output

Once we've done our simple `requests.post` and have a successful API call, we can retrieve the desired information, in 
this case a list of vulnerabilities, from our `response` parameter.

```
response_dict = response.json()
```

Now we have our `response_dict`, which is a dictionary or mapping of key-value pairs, that holds all of the information 
retrieved in the Search call. Though this will contain multiple types of information (such as `metadata` and `links`), 
the data we're looking for will exist under the `data` field in our `response_dict`.

```
vulns = response_dict.get("data")
```

The `data` field contains the data type that was specified in the body of our Search call. In this case, it's 
vulnerability data.

```
{
      "id": "00000000-0000-0000-0000-000000000000",
      "app": {
        "id": "00000000-0000-0000-0000-000000000001"
      },
      "root_cause": {
        "url": "https://website.com/page.txt",
        "method": "GET"
      },
      "severity": "LOW",
      "status": "UNREVIEWED",
      "variances": [
        {
          "original_exchange": {
            "request": "GET /page.txt HTTP/1.1\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.
            8\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: en-US\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.1; 
            WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19\r\nHost: webscantest.com\r\n
            Cookie: TEST_SESSIONID=2h6mp0krvv415m6icqf0qlmpo3; NB_SRVID=srv301408; firstname=John\r\n\r\n",
            "response": "HTTP/1.1 200 OK\r\nConnection: close\r\nDate: Tue, 15 Oct 2019 03:58:30 GMT\r\nContent-Length: 
            84\r\nContent-Type: text/plain\r\nContent-Encoding: gzip\r\nLast-Modified: Mon, 21 Dec 2015 23:35:46 GMT\r\n
            Accept-Ranges: bytes\r\nETag: \"65-52770f2c6d6a3-gzip\"\r\nServer: Apache/2.4.7 (Ubuntu)\r\nVary: 
            Accept-Encoding"
          },
          "module": {
            "id": "00000000-0000-0000-0000-000000000002"
          },
          "attack": {
            "id": "BROWSERCACHECHECK01"
          },
          "message": "Cache-control is missing the no-store directive. Unless specifically constrained by a 
          cache-control directive, a caching system MAY always store a successful response as a cache entry."
        }
      ],
      "links": [
        {
          "rel": "self",
          "href": "https://us.api.insight.rapid7.com:443/ias/v1/search/00000000-0000-0000-0000-00000000000"
        }
      ]
    }
```

There's a lot of information associated with each vulnerability. This includes basic fields like `severity` and 
`status`, as well as details regarding the type of attack performed and the exchange itself.

Looking beyond vulnerabilities, there is a vast array of InsightAppSec information available via the Search endpoint. 
This combined with the option to perform filtering presents the ability to customize and retrieve data as much as  
desired for metrics, reporting, and more.