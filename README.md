# dcacheclient

User and administration interaction with dCache


## Requirements.

Python 3.4+

## Installation & Usage
### pip install

```sh
pip install dcacheclient

```

Otherwise, You can install directly from Github

```sh
pip install git+https://github.com/vingar/dcacheclient.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/vingar/dcacheclient.git`)



## Getting Started with the `dcache-admin` command line

To enable completion:

```
eval "$(register-python-argcomplete dcache-admin)"
```

(cf. https://pypi.org/project/argcomplete/)

Then:

```
dcache-admin --help
```

## Python Client Apis

```
>>> from dcacheclient.client import Client
>>> dcache = Client(url='https://srm.ndgf.org:3880')
>>> dcache.identity.get_user_attributes()
{'status': 'ANONYMOUS'}
>>> dcache.close()
```


## Author

support@dCache.org

