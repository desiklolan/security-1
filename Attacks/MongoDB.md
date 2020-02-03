# MongoDB

This is the MongoDB version of an SQL injection (`' or 1=1 --`). Two things are required:

- An always true condition
- A way to correctly terminate the NoSQL query

MongoDB documentation shows that the SQL `or 1=1` translates to `|| 1==1`. A NULL BYTE will prevent MongoDB from using the rest of the query. In some cases, you can also use comments `//` or ` to comment out the end of the query.

So: ```|| 1==1//```, which with ' (```%27```) around it to complete the query will look like:

```http://example.com/?username=admin%27||%201==1%00%27&password=admin&submit=Submit+Query```

