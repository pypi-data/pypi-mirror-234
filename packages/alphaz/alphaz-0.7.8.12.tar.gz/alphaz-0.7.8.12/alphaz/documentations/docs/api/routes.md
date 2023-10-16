We recommend to add all the route definition in **apis/routes** folder and import all the route definition in **apis/routes/__init__.py**.

Then you will have to import the route in thoe **core.py** file:

```python
from alphaz.models.main import AlphaCore, singleton

@singleton
class Core(AlphaCore):

    def __init__(self,file:str):

        super().__init__(file)

core = Core(__file__)
DB, API, LOG = core.db, core.api, core.log # not required but recommanded

from apis.routes import *
```

# Basic

To specify an api route, juste use the `route` flag:

```python
from alphaz.utils.api import route, api, Parameter

@route("route_name")
def method_name():
    return "hello"
```

Method automatically convert the output to the right format. Default format is `json`

# Description

A description could be specified:

```python
@route("route_name", description="This route say hello")
def method_name():
    return "hello"
```

# Category

The routes are organized by `category`, by default the route category is defined by it **file name**, but it could be specified using the `cat` parameter:

```python
@route("route_name", category="politeness")
def method_name():
    return "hello"
```