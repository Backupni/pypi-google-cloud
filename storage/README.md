Storage
=======

Storage is storage. This is the main component of the system.

Implementation
--------------

- Cloud Storage bucket, which contains Python packages `raw/*.whl`
- Cloud Storage bucket, which contains static site - html `index.html`, `simple/index.html`, `simple/*/index.html` (read PEP 503 to find out more about it: https://www.python.org/dev/peps/pep-0503/) and json's with package metadata `pypi/*/json` (read more here: https://warehouse.readthedocs.io/api-reference/json)
- Cloud Storage bucket, which contains internal metadata for static site generator - package names, package file hashes etc.


FAQ
---

#### Why do I need Proxy service?

Let's test it without `Proxy` and see what happens.

You can serve your static website directly from Cloud Storage bucket.

Enable index pages for your static website bucket:

```
$ gsutil web set -m 'index.html' 'gs://packages-internal.example.com'
```

Add `CNAME` record to your DNS zone. (Name `packages-internal`, target `c.storage.googleapis.com`).

In case you need public PyPI, add permissions to `allUsers`:

1. Select your static bucket `packages-internal.example.com`.
2. Click to `ADD MEMBER` button on `PERMISSIONS` tab. 
3. Set `New members` to `allUsers`.
4. Set `Role` to `Storage Object Viewer`.
5. Click to `SAVE` button. 

Now your PyPi is available at http://packages-internal.example.com. 
But in this case your repository site uses plain http, it's not secure.

You may also access your public repository at https://storage.googleapis.com/packages-internal.example.com/ address. 
But this way is not compatible with index page bucket settings.

If you are going to create private PyPi, this method is also not for you, because of you need basic auth support.

That's why we created `Proxy` service.
