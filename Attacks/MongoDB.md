# MongoDB

This is the MongoDB version of an SQL injection (`' or 1=1 --`). Two things are required:

- An always true condition
- A way to correctly terminate the NoSQL query

MongoDB documentation shows that the SQL `or 1=1` translates to `|| 1==1`. A NULL BYTE will prevent MongoDB from using the rest of the query. In some cases, you can also use comments `//` or ` to comment out the end of the query.

So: ```|| 1==1//```, which with ' (```%27```) around it to complete the query will look like:

```http://example.com/?username=admin%27||%201==1%00%27&password=admin&submit=Submit+Query```

----------------

In this example, we will try to retrieve more information from the NoSQL database.

Using a bit of guess work (or previous knowledge of the application), we can deduce that there is probably a `password` field.

We can play around to confirm that guess:

- if we access ```/?search=admin'%20%26%26%20this.password.match(/.*/)%00```: we can see a result.
- if we access ```/?search=admin'%20%26%26%20this.password.match(/zzzzz/)%00```: we cannot see a result.
- if we access ```/?search=admin'%20%26%26%20this.passwordzz.match(/.*/)%00```: we get an error message (since the field `passwordzz` does not exist).

Now, we have a way to perform a blind injection since we have two states:

- No result when the regular expression does not match something: `false` state.
- One result when the regular expression matches something: `true` state.

Using this knowledge, we can script the exploitation to retrieve the `admin` password. We will first ensure that the matching is done correctly by using: `^` and `$` to make sure we do not match characters in the middle of the string (otherwise iterating will be far harder).

The algorithm looks like:

- test if password match /^a.*$/ if it matches test without the wildcard `.*`(to check if it's the full password). Then move to the next letter if it does not match.
- test if password match /^b.*$/ if it matches test without the wildcard `.*`. Then move to the next letter if it does not match. 

For example, if the password is `aab`, the following test will be performed:

- `/^a.*$/` that will return true.
- `/^a$/` that will return false.
- `/^aa.*$/` that will return true.
- `/^aa$/` that will return false.
- `/^aaa.*$/` that will return false.
- `/^aab.*$/` that will return true.
- `/^aab$/` that will return true. The password has been found.

With these details, you should be able to retrieve the password for the user `admin`. The password is the key to solve this exercise so it should have the following format: `XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX`, where X can be `[0-9a-f]`.