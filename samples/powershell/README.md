# API Overview

Throughout each of our PowerShell InsightAppSec API examples, there are a few concepts that are consistently applicable, 
regardless of the endpoint or the data associated with it. These include:

1. Reusable Variables
2. Parameters
3. API Request

We'll walk through each of these sections in detail to provide a better understanding of them and how they will apply 
across all of our InsightAppSec API examples. This will also aid in ensuring we adhere to API best practices.

We'll then look at two other concepts that need to be addressed.

1. Error handling
2. Pagination

## Reusable Variables
In PowerShell, it is common to make multiple API requests in one script. To facilitate this, some data that will be
reused across all API requests can be saved as variables.

The first parameter that will always be required is the base URL. The base URL is determined by your region.
If you're uncertain of your region, a complete listing of them is available [here](https://insight.help.rapid7.com/docs/product-apis#section-supported-regions).
For our examples, we will use the US region.

```
$baseUrl = 'https://us.api.insight.rapid7.com/ias/v1/'
```

Another parameter that will always be required is the InsightAppSec API key. This key is used in authenticating to the
Rapid7 InsightAppSec API and is a necessity for every single API call. It can be set as a string parameter and will 
later be used when performing a request. Rapid7 recommends the encryption and secure storage of sensitive values such 
as this one to ensure best security practices, but we have it displayed in this manner for readability purposes.

```
$apiKey = 'Your-API-key-here'
```

The next request-related parameter that must be defined is the `header`. Headers can be used to pass additional 
information that's needed to make an API request. In this case we need to pass our InsightAppSec API key as a header 
called `X-Api-Key` to perform authentication.

Another `header` we'll need is `Content-Type`, which is used in `POST` or `PUT` requests to indicate the type of data 
being sent. For InsightAppSec API requests, it's best to use the `application/json` content type.
Note that while not required for other request types, including this header will not cause issues.

With these headers in mind, we can create a dictionary (which is a set of key-value pairs) that will hold values for 
both the `X-Api-Key` and `Content-Type` fields.

```
$headers = @{'X-Api-Key' = $apiKey, 'Content-Type' = 'application/json'}
```

To summarize, the fields required for performing an API request are the base URL,
The InsightAppSec API key, and the content type. Together, these last two form the headers.

```
$baseUrl = 'https://us.api.insight.rapid7.com/ias/v1/'
$apiKey = 'Your-API-key-here'
$headers = @{'X-Api-Key': $apiKey, 'Content-Type': 'application/json'}
```

## Parameters
Next we need to build a parameters dictionary to hold the information that will be used to create the API request.
The parameters will consist of three to four parts depending on the API call. Let's look at two examples.

#### IMPORTANT
The keys for this dictionary correspond to expected input names in the PowerShell RestMethod cmdlet.
Changing these key names will result in the script not functioning correctly.

```
@params = @{
Uri = $baseUrl + 'apps' + ?q=index=0,size=50,sort=app.name,ASC
Headers = $headers
Method = 'GET'
```

```
@params = @{
Uri = $baseUrl + 'search'
Headers = $headers
Method = 'POST'
Body = @{'type'='app', 'query'='some string'}
```

The first part is called `Uri`. This is the API URL + the API endpoint + any URL parameters, if applicable.
URL params will be explained in the pagination section.

Next are the `Headers`. This is simply the headers variable defined earlier.

After this comes the `Method`. The method can be `GET` `POST` `PUT` or `DELETE`

For `POST` and `PUT` calls, an additional part is often needed called the `Body`.
 The body contains information in the form of a dictionary that will be used in the request.


## API Request
Finally, the request must be run. In PowerShell this is very easy.
```
$output = Invoke-RestMethod @params
``` 

This line runs the `Invoke-RestMethod` cmdlet with the `@params` dictionary as input.
It then saves the output as a variable named `$output`

## Error Handling
As mentioned in the overview, we will cover additional concepts in this document to ensure that their
use is understood for later examples. The first of these is error handling.

In PowerShell by default a non 2xx status code on the API call return will raise an error.
When an error is raised two things will happen. First the error information will be displayed in the shell as stderr.
This will appear as red text with the error message and the line of code that caused the error.
The error message will also be appended to the default variable `$error`. The error variable is a list of all
errors that have occurred in a specific PowerShell session.

For more advanced error handling you can use a try catch block. For example:
```
try {
    $output = Invoke-RestMethod @params
}
catch {
$statusCode = $_.Exception.Response.StatusCode.value__ 
}
if ($statusCode -eq 401) {
    <Error handling code here>
}
```

Some example error codes you may experience are:
* 401: your API key is incorrect or invalid
* 403: your API key is not granted access to the requested operation or element
* 404: Content not found or doesn't exist

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

How much and in what order this data is retrieved can be modified by the URL parameters.
Recall in the `GET` example above, the following string was appended to the URL: `?q=index=0,size=50,sort=app.name,ASC`
This data controls pagination, with `size=50` being how many results are retrieved per index page.
`index=0` tells us we want to retrieve the first page, in this case out of 17.
`sort=app.name,ASC` tells the API we want the list of data sorted by application name in ascending alphabetical order.

The below code snippet may be used as a starting place for pagination within our data retrieval `Do Until` loop. For instance,
you will find this used in the example for the `Search` endpoint.

```
# If more data is left, get next URI
If ($vulns.Length -lt $output.metadata.total_data){
    # set URI for next page of data
    for ($i=0; $i -lt $output.links.Length; $i++){
        if ($output.links[$i].rel -eq 'next') {
            $uri = $output.links[$i].href
            break
        }
    }
}
Else { # End data retrieval
    $continue = $false
}
```

This code simply checks to see if `$vulns` (which in this case is a list containing vulnerability data) contains the full dataset,
and, if it does not, finds the next URI to make a request to in order to get the next "page" of results.

## Conclusion

With each of these concepts being applicable across the InsightAppSec API, we now have a solid foundation for delving 
into individual endpoints and further understanding their usage. Read on to check out the walkthroughs we've created 
for some specific InsightAppSec API endpoints.
