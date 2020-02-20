# SSRF

A **Server Side Request Forgery** vulnerability allows an attacker to gain access to internal web server resources by getting the server to make HTTP requests on our behalf. This can be used to access internal pages, perform network scans, etc.

As an example, trying to retrieve the content of the webroot of a server listening on port TCP/1234. We can't access the service directly but we can get the vulnerable server to do it for us. So if the initial url was:

```http://example.com/?url=https://assets.example.com/```

We might change it to:

```http://example.com/?url=http://localhost:1234/```. 

Decimal IP addresses may help avoid filters here: https://www.smartconversion.com/unit_conversion/IP_Address_Converter.aspx. Eg:

```http://example.com/?url=http://2130706433:1234/```

Another mechanism to bypass a filter is to create a zone with a subdomain that responds to anything under it as 127.0.0.1, or the target IP, and then to add that to the end of the filtered domain.