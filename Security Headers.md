### XSS Payloads

<script>alert('Honk')</script>
```html
<svg onload="document.body.innerHTML='<img src=//cdn3.dualshockers.com/wp-content/uploads/2019/10/maxresdefault-2.jpg>'">
```



```powershell
<customHeaders>
        <add name="X-Frame-Options" value="sameorigin" />
        <add name="X-XSS-Protection" value="1" />
        <add name="X-Content-Type-Options" value="nosniff" />
        <remove name="Server" />
        <remove name="X-Powered-By" />
        <remove name="X-AspNet-Version" />
        <remove name="X-AspNetMvc-Version" />
        <add name="Strict-Transport-Security" value="max-age=2592000" />
```