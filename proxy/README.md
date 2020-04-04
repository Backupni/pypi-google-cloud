Proxy
=====

This service adds basic auth with tokens support and provides access to packages. Simple layer between Storage and end users.

Implementation
--------------

- managed Google Cloud Run
  - uses Python image with Starlette Python ASGI framework (it should be fast)
  - uses Service Account
  - uses Google Cloud Secret for auth tokens storage
  - (optional) uses custom domain name
