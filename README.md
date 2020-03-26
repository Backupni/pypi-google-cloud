Private PyPI - Google Cloud
===========================

Private PyPI repository on top of Google Cloud Platform. 

You need basic Python skills and Google Cloud account to continue.


Project Goals and Decisions
---------------------------

### Secure

- modular design
- simple modules, without tons of unused code and API endpoints (code review should be easy)
- static whenever it possible

### Optimised for Google Cloud

- uses Google Cloud Platform for any related compute, storage or network operations to provide best user experience

### Best choice for Python perfectionists
- respects PEPs (PEP 503)
- uses tokens instead of username & passwords (follow PyPi suggestions)
- supports package hashes (hello, poetry)


Structure: Project Services and Components
------------------------------------------

Just 4 simple components. Click to links and follow guides.

### Storage

Storage is storage. This is the main component of the system.

### Builder

This service updates your static repository.

### Proxy

This service adds basic auth with tokens support and provides access to packages. Simple layer between Storage and end users.

### Uploader

This service uploads new packages to your storage and invokes Builder.


Alternatives
------------

If you would like to use cloud agnostic solution, check this repositories:
- stevearc/pypicloud
- private-pypi/private-pypi
