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

Just 4 simple components.

### Storage

Storage is storage. This is the main component of the system. [Read more...](storage)

### Builder

This service updates your static repository. [Read more...](builder)

### Proxy

This service adds basic auth with tokens support and provides access to packages. Simple layer between Storage and end users. [Read more...](proxy)

### Uploader

This service uploads new packages to your storage and invokes Builder. [Read more...](uploader)


Install
-------

Click to banner and follow installation instructions (2 required and 2 optional simple steps inside).

[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://ssh.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fbackupner%2Fpypi-google-cloud&cloudshell_print=cloud-shell-readme.txt&cloudshell_open_in_editor=pypi.yaml&cloudshell_working_dir=install&cloudshell_tutorial=install.md)


Uninstall
---------

- (Recommended) Just delete your private PyPi project. 

  ```sh
  gcloud projects delete 'YOUR_PROJECT_ID'
  ```
- (Alternative) If you use shared project run this command:

  ```sh
  gcloud deployment-manager deployments delete \
      'pypi' \
      --project='YOUR_PROJECT_ID'
  ```

  You should also check assigned roles for `YOUR_PROJECT_NUMBER@cloudservices.gserviceaccount.com` and `YOUR_PROJECT_NUMBER@cloudbuild.gserviceaccount.com` service accounts.


License
-------

This source code is licensed under Apache 2.0. Full license text is available in [LICENSE](LICENSE).


Alternatives
------------

If you would like to use cloud agnostic solution, check this repositories:
- `stevearc/pypicloud`
- `private-pypi/private-pypi`
