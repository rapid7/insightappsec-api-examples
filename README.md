# Rapid7 InsightAppSec API Examples

This project seeks to demonstrate proper usage of the InsightAppSec API via both generic examples that showcase a 
variety of endpoints, as well as specific use cases that can be applied within an organization. Included is a complete 
guide to getting started with the InsightAppSec API, as well as navigation of its documentation, API usage and 
configuration, and implementation of practical use cases across multiple endpoints. All examples and use cases will 
either be Python or PowerShell-based, with more language support in the future based on interest.

More information about InsightAppSec can be found here: https://www.rapid7.com/products/insightappsec/

# Table of Contents
1. [Getting Started](#getting-started)
2. [API Basics](#api-basics)
3. [InsightAppSec API Examples](#insightappsec-api-examples)
4. [InsightAppSec Use Cases](#insightappsec-use-cases)

## Getting Started

### Generating an API Key

To interact with the Rapid7 InsightAppSec API, you'll need an API key. Below are the steps for generating a new API key.

1. Login to the Rapid7 Insight Platform
2. Click the gear icon at the top right of the page
3. Select `API Keys`
4. Select either `New User Key` or `New Organization Key` (can be toggled with the lefthand menu). If you're uncertain 
which type of key to generate, keep in mind:
  - All roles are able to generate a user key. This key is associated with your account and will track all changes and 
  actions that you make.
  - Only platform admins can generate an organization key. This is a "super key" and can do everything in the API 
  across all products.
5. Once generated, be sure to copy and securely store the key, as it cannot be accessed again later

As stated before, this API key will allow you to begin interacting with the Rapid7 InsightAppSec API. More 
specifically, the API key is used in authenticating to your instance of InsightAppSec and performing transactions 
within that context. The key will be will be passed as part of every API request via a single HTTP header: `X-Api-Key`. 
Additional details about the API key and this header are provided later in the guide.

### InsightAppSec API Documentation

Full documentation for the Rapid7 InsightAppSec API is available here: https://help.rapid7.com/insightappsec/en-us/api/v1/docs.html

When navigating the document, use the menu on the lefthand side to select the InsightAppSec component you'd like more 
info on, and then further narrow that by selecting individual API operations. You can also search the API documentation 
by keyword.

Each individual operation section will contain details on URL path, API parameters, request body (if required), and 
response samples. All of these can be used to construct an API request and perform the associated operation in the 
context of InsightAppSec.

Note that the beginning of the API documentation guide also contains additional info on permissions, 
searching/filtering, API errors, and query parameters that can be used in API requests.

#### OpenAPI/Swagger Specification

Along with the HTML generated documentation, an OpenAPI/Swagger spec is made available and can be used for auto 
generating API clients or for use in Postman.  The spec can be downloaded from https://help.rapid7.com/insightappsec/en-us/api/v1/insightappsec-api-v1.json. 
Usage of this file in conjunction with a tool such as Postman can be key for better familiarizing with a new API.

#### Accessing the API Via Postman

Postman is an API client that provides a simple user interface to allow for API interaction. It can be used in 
conjunction with the InsightAppSec API spec file to automatically generate requests to perform API calls. The following 
steps can be used to import the spec file into Postman. This will automatically generate requests to perform API calls, 
and is extremely useful when initially getting familiar with a new API endpoint.

1. Open Postman
2. Select `Import` at the top left
3. Select `Choose File` and select the InsightAppSec spec file that was downloaded in [the previous section](#openapiswagger-specification)
4. Select the new InsightAppSec API section that's now available under Collections

Under this newly imported InsightAppSec API Collection, you can see an entry listed for each component that exists in 
InsightAppSec. If you expand the options and select a specific operation, a pre-formatted request will appear on the 
right that contains the operation type, the URL path, the body (if needed), and any necessary headers.

Although this pre-formatted request does contain the majority of the required fields for making an API call, there are 
a couple fields that need to be updated. The following steps can be used to make a request in Postman, when utilizing 
the imported spec file.

1. Select an operation from the InsightAppSec Collection
2. In the URL field, replace the {{baseurl}} with the correct value (https://[region].api.insight.rapid7.com/ias/v1)
3. Update any placeholder query parameters in the URL, such as `index` and `sort`. If you're uncertain of these 
parameters, you can remove them from the URL entirely (including the `?`).
4. Under the Headers tab add a new header, where the key is `X-Api-Key` and the value is your previously generated API 
key
5. Update any placeholder values in the request Body (if any), denoted with text such as `<string>`
6. Select the `Send` button to make the request
7. Observe the response received. A status code in the `200` range will mean the request was successful. If it failed, 
the response may contain an error message denoting the reason.

Use these steps with any additional calls to better familiarize with the InsightAppSec API, while also keeping in mind 
that some are more sensitive than others (such as `DELETE` operations).

## API Basics

In simple terms, an API is something that allows applications to communicate with one another. In this case, we'll be 
communicating with InsightAppSec via its API to perform basic actions. These actions allow us to automate 
functionality within InsightAppSec that would normally be considered manual.

There are several basic API concepts that are applicable to the InsightAppSec API, as well. It can be beneficial to 
review these concepts before utilizing the API to gain a better understanding of best practices.

### Methods

Methods are different types of actions that can be performed in the context of an API call. In other words, it 
determines what operation will be performed upon the specified resource. There are four common API methods that are 
used in the examples throughout this project.

`GET` - Used for retrieving information, and NOT for modifying it. For example, a call to the Get Apps endpoint would 
return a list of applications and their associated details from InsightAppSec.

`POST` - Used to create new resources, based on data the user provides. For example, a call to the Create Blackout 
endpoint would result in a brand new blackout being created in InsightAppSec, based on the data provided.

`PUT` - Used to update an existing resource, based on some identifier that the user provides. For example, a call to 
the Update Scan Config endpoint requires a scan config ID to be specified, and would result in that config being 
modified based on the data provided.

`DELETE` - Used for deleting resources. For example, a call to the Delete Schedule endpoint requires a schedule ID 
and would result in the associated schedule being deleted. Use with caution, as it can result in the permanent loss of 
data.

### Headers

Headers are used in API requests to supply additional information about the API call itself. This can include info 
relating to authorization, caching, and the type of content being supplied in the call. A couple headers commonly 
used in InsightAppSec API requests are for authorization and content-type.

```
headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}
```

The `X-Api-Key` header allows authentication to the InsightAppSec API, while the `Content-Type` header specifies that 
a JSON body will be supplied in the request.

### Parameters

Parameters are another variable part of an API call. A parameter is an additional field that can be supplied in an API 
request to specify a particular resource, or otherwise influence the results of the call.

For instance, when making a call to the InsightAppSec Get Vulnerability endpoint, a vulnerability ID must be provided 
to specify the vulnerability to retrieve. Without that parameter, the API would not be able to determine which 
vulnerability to return.

Another parameter available in the context of InsightAppSec API calls is `sort`. Adding the `sort` parameter to a 
request will result in the response being sorted accordingly. For example, when retrieving scans via the Get Scans 
endpoint, `sort` could be used as below to specify that scans should be returned in descending order of the scan's 
submit time.
 
```
sort=scan.submit_time,DESC
```

### Body

A request body is a list of key-value pairs used to send information when making an API call. A body is typically 
required with `POST` and `PUT` requests to specify info about the resource that is being created or updated.

For instance, when using the InsightAppSec Create Blackout endpoint, a body must be provided so the API knows what 
details to use when creating the blackout. This includes information like the name and the time at which the blackout 
occurs, as well as the application it's associated with (if any). 

An example JSON body typically resembles the following:

```
{
  "name": "Name 1",
  "description": "This is a description.",
  "type": "Type 1"
}
```

The fields before the colon are the keys, while the fields afterwards are the values. The result is the creation or 
updating of a resource with each field being given its specified value.

The type of data required in the body will vary based on the endpoint being utilized, as there will always be fields 
that differ between different types of resources.

## InsightAppSec API Examples

In this project's `samples` directory, we have taken several InsightAppSec API endpoints and created simple example 
scripts for them in Python and PowerShell.

For both [Python](samples/python/README.md) and [PowerShell](samples/powershell/README.md), there is an accompanying 
guide that covers general InsightAppSec API concepts and best practices when it comes to using the API. It can be 
helpful to start with this guide to gain a better understanding of recurring concepts like parameters and pagination.

Each example includes a script that demonstrates the use of that endpoint. Every script is in a working state, meaning 
that it can be executed to retrieve or modify existing InsightAppSec data. All that's needed is an InsightAppSec API 
key, and any parameters relevant within the context of that endpoint.

Also included with each example is a README that walks through the configuration and usage of that endpoint in detail. 
This includes guidance on formatting the endpoint URL, parameters, and how to process the response received in the API 
call. Follow along with this README to get a step-by-step walkthrough of writing a script to utilize that endpoint.

## InsightAppSec Use Cases

To help better illustrate concrete ways in which the InsightAppSec API can be used within an organization, we've 
created a few solutions that harness the API's capabilities to fulfill realistic use cases. Each solution is fully 
functional and includes its own configuration options, along with documentation to understand its usage. These are all 
located under the `automation_use_cases` directory.

### InsightAppSec Reporting

The InsightAppSec Reporting solution is designed to generate reports based on scan data retrieved from InsightAppSec, 
driven by a set of user-defined configurations. This allows teams to automate the process of report generation, and 
provides a level of flexibility to perform this generation for as many application/configuration pairings as needed.

### Application Onboarding

The Application Onboarding solution provides a way to automate the creation of new applications in InsightAppSec. 
This is particularly beneficial if the user has a large number of applications that must be configured within 
InsightAppSec, as it is flexible and configuration-driven.

### Scan Automation
The Scan Automation solution allows users to automate the launching and monitoring of an application scan, based on 
the provided names for the application and scan configuration. Scan automation can be vital for usage in build/release 
pipelines and in general as part of an efficient organization's software development life cycle. 