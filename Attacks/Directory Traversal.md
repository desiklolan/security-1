# Directory Traversal

Directory traversals come from a lack of filtering/encoding of information used as part of a path by an application.

As with other vulnerabilities, you can use the "same value technique" to test for this type of issue. For example, if the path used by the  application inside a parameter is `/images/photo.jpg`. You can try to access:

- `/images/./photo.jpg`: you should see the same file.
- `/images/../photo.jpg`: you should get an error.
- `/images/../images/photo.jpg`: you should see the same file again.
- `/images/../IMAGES/photo.jpg`: you should get an error (depending on the file system) or something weird is going on.

If you don't have the value `images` and the legitimate path looks like `photo.jpg`, you will need to work out what the parent repository is.

### Linux

Once you have tested that, you can try to retrieve other files. On Linux/Unix the most common test case is the `/etc/passwd`. You can test: `images/../../../../../../../../../../../etc/passwd`, if you get the `passwd` file, the application is vulnerable. The good news is that you don't need to know the number of `../`. If you put too many, it will still work.

```../../../../../../../../../../../../../../../../etc/passwd```

### Windows

If you have a directory traversal in Windows, you will be able to access `test/../../../file.txt`, even if the directory `test` does not exist. This is not the case, on Linux. This can be really  useful where the code concatenates user-controlled data, to create a  file name. For example, the following PHP code is supposed to add the  parameter `id` to get a file name (`example_1.txt` for example). On Linux, you won't be able to exploit this vulnerability if there is no directory starting by `example_`, whereas on Windows, you will be able to exploit it, even if there is no such directory.

```
 $file = "/var/files/example_".$_GET['id'].".txt";
```

```../../../../../../../../../../../../../../../../windows/win.ini```



In this example, based on the header sent by the server, your browser will display the content of the response. Sometimes the server will  send the response with a header `Content-Disposition: attachment`, and your browser will not display the file directly. You can open the  file to see the content. This method will take you some time for every  test.

Using a Linux/Unix system, you can do this more quickly, by using `wget` or `curl`.



In this example, you can see that the full path is used to access the file. However, if you try to just replace it with `/etc/passwd`, you won't get anything. It looks like a simple check is performed by  the PHP code. You can however bypass it by keeping the beginning of the  path and add your payload at the end, to go up and back down within the  file system.



This example is based on a common problem when you exploit directory traversal: the server-side code adds its own suffix to your payload. This can be easily bypassed, by using a NULL BYTE (which you need to URL-encode as `%00`). Using NULL BYTE to get rid of any  suffix added by the server-side code is a common bypass, and works  really well in Perl and older versions of PHP (< 5.3.4).