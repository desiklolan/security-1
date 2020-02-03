**StarRez:** We should verify the redirect, like we do when logging in (AuthenicationHelper.SanitiseUrl), so that the user not redirected to a malicious website. This should be done for all redirects.

**Audit logged as:** https://jira.starrez.com/browse/BUG-679

 

\--------------------------------------------------------------------------------------------------------------------------------------------------

# Testing

(iFrameUrl)

[https://pentest.starrezhousing.com/StarRezPortalX/admin/ExitEditOr?%69%46%72%61%6d%65%55%72%6c=%2f%2f%78%6b%63%64%2e%63%6f%6d](https://pentest.starrezhousing.com/StarRezPortalX/admin/ExitEditOr?iFrameUrl=%2f%2fxkcd.com)

 

(returnUrl)

https://localhost/StarRezPortalX/Auth/LoginPage?returnUrl=https://xkcd.com

 

-------------------------------------------------------------------------------------------------

 

You can abuse protocol-relative urls, making PortalX think that it is a relative URL, but in reality it's an absolute URL with a relative protocol. Proof of exploit: 

 

https://pentest.starrezhousing.com/StarRezPortalX/admin/exiteditor?iframeurl=//xkcd.com

 

\--------------------------------------------------------------------------------------------------------------------------------------------------

 

Secondly, the iframe url looks to do a contains, meaning if we own a domain that is part of the customers domain, eg, "housing.com" against "cust.starrezhousing.com" we can fool the url check.

Proof of exploit: https://pentest.starrezhousing.com/StarRezPortalX/admin/exiteditor?iframeurl=https://housing.com/in/buy/real-estate-mumbai

Redirects to [https://housing.com/in/buy/real-estate-mumbai](https://pentest.starrezhousing.com/StarRezPortalX/admin/exiteditor?iframeurl=https://housing.com/in/buy/real-estate-mumbai), as they are both over https, and 'pentest.starrezhousing.com' contains 'housing.com'

 

\--------------------------------------------------------------------------------------------------------------------------------------------------

 

For open redirects, try using this character: 。The website thinks it's redirecting to a page on the site, but browsers convert it to a '.' thus completing the redirect. 

 

Usage: ?url=//google。com

Goes to: [https://google.com](https://t.co/NeH0AFZR2O?amp=1)

URL encoded: %E3%80%82

 

\--------------------------------------------------------------------------------------------------------------------------------------------------

 https://deploymentmonitor.starrezcloud.io/history?next=whitelisted.com&next=google.com



# Payload Examples

 

[https://github.com/swisskyrepo/PayloadsAllTheThings/blob/2a4c4f46b2dae8ed15bd7f340c5cb013ddb72f9a/Open%20Redirect/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/2a4c4f46b2dae8ed15bd7f340c5cb013ddb72f9a/Open Redirect/README.md)