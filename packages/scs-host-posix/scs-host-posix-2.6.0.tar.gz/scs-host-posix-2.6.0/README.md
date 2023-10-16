# scs_host_posix
Host abstractions for data consumers running POSIX-compliant operating systems, including Windows 10.

_Contains library classes only._

**Required libraries:** 

* Third party (always required): AWSIoTPythonSDK, tzlocal
* Third party (to enable OSIO data access) paho-mqtt, pycurl
* SCS root: scs_core


**Branches:**

The stable branch of this repository is master. For deployment purposes, use:

    git clone --branch=master https://github.com/south-coast-science/scs_host_posix.git
