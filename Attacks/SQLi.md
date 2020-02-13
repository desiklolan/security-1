# SQL injections

[TOC]
SQL injections are one of the most common (web) vulnerabilities. All  SQL injections exercises, found here, use MySQL for back-end. SQL  injections come from a lack of encoding/escaping of user-controlled  input when included in SQL queries.

Depending on how the information gets added in the query, you will need different things to break the syntax. There are three different ways to echo information in a SQL statement:

- Using quotes: single quote or double quote
- Using back-ticks
- Directly

The way information is echoed back, and even what separator is used will decide the detection technique. However, you don't have this information, and you will need to try to guess it. You will need to formulate hypotheses and try to verify them. That's why spending time poking around with these examples is so important.

In this challenge, you will need to bypass the login page using SQL injection. The SQL query looks something like:

```
SELECT * FROM user WHERE login='[USER]' and password='[PASSWORD]';
```

'Where: `[USER]` and `[PASSWORD]` are the values you submitted.

The logic behind the authentication is:

- if the query returns at least one result, you're in
- if the query returns no result, you have not provided a valid username and password.

Our goal is to make the query return at least one result. To do so we are going to inject a condition that is always true: `1=1`. To do that, we are going to:

- Break outside of the single quote to be able to inject SQL using a single quote.
- Add a `OR` keyword to make sure the comparison is always true.
- Add our always true comparison: `1=1`
- Comment out the remaining query using `--` (the space at the end matters) or `#`.

If we put everything together, we get our payload: ```admin' OR 1=1 -- ```. Try ```"``` as well. 



#### LIMIT=1;

If the code checks for multiple results being returned, you can evade with ```LIMIT 1;```. The resulting payload looks like ```admin' OR 1=1 LIMIT 1; -- ```



#### Error: NO SPACE

Sometimes the error message gives away the protection created by the developer: `NO SPACE`. This error message appears as soon as a space is injected inside the request. It prevents us from using the `' or '1'='1` method, or any fingerprinting that uses the space character. However, this filtering is easily bypassed, using tabulation (HT or `\t`). You will need to use encoding, to use it inside the HTTP request. An example payload looks like this: ```'	OR	1=1	LIMIT=	1;	--	```. A tab ```	``` encodes as ```%09```.



#### No Spaces or Tabs Allowed

This filter can be bypassed with URL encoding ```%20```. Alternately us ```+``` between characters.



#### GBK

This is a rare issue that provides a way to bypass `addslashes`. It relies on the way MySQL performs escaping and the charset used by the connection. If the database driver is not aware of the charset used it will not perform the right escaping and create an vulnerability. This exploit relies on the usage of [GBK](https://en.wikipedia.org/wiki/GBK_(character_encoding)), which is a character set for simplified Chinese. Using the fact that the database driver and the database don't match charsets, it's possible to generate a single quote and break out of the SQL syntax to inject a payload.

Using the string `\xBF'` (URL-encoded as `%bf%27`), it's possible to get a single quote that will not get escaped properly. It's therefore possible to inject an always-true condition using `%bf%27+or+1=1+--+` and bypass the authentication.

This issue can be remediated by setting the connection encoding to 'GBK' instead of using an SQL query (which is the source of this issue). Here the problem comes from the execution of the following query:

```
SET CHARACTER SET 'GBK';
```

See http://shiflett.org/blog/2006/addslashes-versus-mysql-real-escape-string.








## Dynamic query in application
### Potential String Injection

"select * from users where name = '" + userName + "'";

### Potential Numeric Injection

"select * from users where employee_id = " + userID;

## Attacker supplies unexpected text

- userName = **Smith' or '1'='1**
- userName =**' or 1=1 --**
- userID = **1234567 or     1=1**
- UserName = **Smith’;drop     table users; truncate audit_log;--**

## Application executes query

- ```select * from users where name = 'Smith' or '1' = '1'```

- ```select * from users where name = 'Smith' or TRUE```

- ```select * from users where employee_id = 1234567 or 1=1```


**All records are returned from database**

## Special Characters

/* */     are inline comments
 -- , #      are line comments

Example: Select * from users where name = 'admin' --and pass = 'pass'

 

;    allows query chaining

Example: Select * from users; drop table users;

 

',+,||     allows string concatenation
 Char()     strings without quotes

Example: Select * from users where name = '+char(27) or 1=1

## Special Statements

Unions allows overlapping of database tables 'Select id, text from news union all select name, pass from users'

Joins allows connecting to other tables

## Defences against SQL injection
- Parameterized Queries
- Stored Procedures
- Use Encoders (owasp esAPI)

For non-SQL injections, encoding is required.