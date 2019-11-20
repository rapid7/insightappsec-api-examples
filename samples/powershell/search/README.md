# Search

## Endpoint Overview

The Search endpoint is incredibly flexible and perhaps one of the most powerful endpoints within the InsightAppSec API. 
It can be used to filter and retrieve a variety of information based on a user-provided query.

While additional endpoints do exist in the InsightAppSec API for retrieving specific data (say, a particular scan), 
Search broadens your capabilities by allowing the retrieval of data across different InsightAppSec components. For 
instance, searching vulnerabilities based on a particular scan ID, or searching completed scans based on a given date 
range. This usage of queries makes it easy to obtain the exact type of data you're looking for.

## API Request
The Search endpoint contains a couple of unique components that we'll review here.

We will begin by defining the URI of the endpoint we will be requesting data from. The `$api_url` is defined as follows:

```
$api_url = "https://$region.api.insight.rapid7.com/ias/v1/"
```

We also need to specify our `$api_endpoint` parameter to have a complete URL for the API call, and in the case of this endpoint, it's `search`. We will use `$full_url` for our request.

```
$api_endpoint = "search"
$full_url = api_url + api_endpoint
```

Although Search is an endpoint used to retrieve data, it is a `POST` request. This means that, in addition to utilizing 
the standard parameters that are detailed in our [API Overview](../README.md), we will also need to provide a body for 
the request. The body we provide will contain two things: the type of data we want, and the query that will filter that 
data.

Here's an example body that we can use in this API call:

```
$body = @{
    "type": "VULNERABILITY",
    "query": "vulnerability.scans.id='00000000-0000-0000-0000-000000000000'"
}
$body = $body | ConvertTo-Json
```

This body will tell the API to retrieve all vulnerabilities from the given scan ID. This is a useful reporting-type query for obtaining a scan's vulnerabilities without actually accessing InsightAppSec via the UI. Note the single quotes around the `vulnerability.scans.id` value provided, as these are required for proper query formatting. Additionally, note that we must explicitly convert the body to JSON format so our request can be handled correctly.

Also note that this is just one possibility of many for search queries. Check out the [Search Catalog](https://help.rapid7.com/insightappsec/en-us/api/v1/docs.html#tag/Search)
along with the accompanying operators and examples to view a complete listing of query options.

Now that we have defined our body, we will want to make sure our headers are set properly. This means setting your API key and setting the `Content-Type` key to `application/json` to let the endpoint know you are sending it JSON. We use the following to set the headers:

```
$apiKey = 'your-api-key-here'
$headers = @{
    'X-Api-Key' = $apiKey; 'Content-Type' = 'application/json'
}
```

With all of our other standard parameters assigned, performing the request is simple and requires the usage of the `Invoke-RestMethod` function. 

```
$vulns = @()
$output = Invoke-RestMethod -Uri $uri -Headers $headers -Body $body -Method 'POST'
```

`$vulns` will be a list of vulnerabilities we build from the `$output` variable which contains all of the data retrieved from the endpoint.


## Output
Now that we have our output, let's extract some data. `$output` is a mapping of key-value pairs holding all of the information retrieved during our Search call. The keys are `data`, `metadata`, and `links`. Right now we are interested in `data` because, for our query, it holds a list of vulnerabilities (as we defined in the `type` key of our query). The first thing we will want to do is add the contents of `$output.data` to our `$vulns` list. Doing so is simple:

```
$vulns = $vulns + $output.data
```

By now, `$vulns` should contain some data. The following is the result to `stdout` displayed in the terminal when running `echo $vulns`:

```
id         : 00000000-0000-0000-0000-000000000000
app        : @{id=00000000-0000-0000-0000-000000000000}
root_cause : @{url=http://webscantest.com/datastore/; parameter=Set-Cookie: TEST_SESSIONID; method=GET}
severity   : LOW
status     : UNREVIEWED
variances  : {@{original_value=Set-Cookie: TEST_SESSIONID=c2hrattvgaaharsekouu4s0gg6; path=/; original_exchange=; module=; attack=}}
links      : {@{rel=self; href=https://us.api.insight.rapid7.com:443/ias/v1/search/00000000-0000-0000-0000-000000000000}}

id         : 00000000-0000-0000-0000-000000000000
app        : @{id=00000000-0000-0000-0000-000000000000}
root_cause : @{url=http://webscantest.com/datastore/search_double_by_name.php; method=GET}
severity   : INFORMATIONAL
status     : UNREVIEWED
variances  : {@{original_exchange=; module=; attack=; message=The X-XSS-Protection HTTP response header not found.}, @{module=; attack=; message=The X-XSS-Protection HTTP response header not found.}, 
             @{module=; attack=; message=The X-XSS-Protection HTTP response header not found.}}
links      : {@{rel=self; href=https://us.api.insight.rapid7.com:443/ias/v1/search/00000000-0000-0000-0000-000000000000}}
```

There's a lot of information associated with each vulnerability. This includes basic fields like `severity` and 
`status`, as well as details regarding the type of attack performed and the exchange itself.

Looking beyond vulnerabilities, there is a vast array of InsightAppSec information available via the Search endpoint. 
This combined with the option to perform filtering presents the ability to customize and retrieve data as much as  
desired for metrics, reporting, and more.