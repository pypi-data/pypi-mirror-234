# Introduction

The api system is completely based on Flask and compatible with it. 
You could use Flask inside Alpha system without any issue.

## Launch

To start the api execute the `api.py` file

```sh
python api.py
```

!!! note
    set `ALPHA_CONF` environment parameter is you want to set the environment.

Verify the deployment by navigating to your server address in your preferred browser:

```sh
127.0.0.1:<port>
```

## How to use

Your could import it using simply from the **utils**:

```python
from alphaz.utils.api import api
```

or from the **core** if you are using it

```python
from core import core, API
```

> **api** / **API** is the equivalent for **app** in **Flask** framework.
