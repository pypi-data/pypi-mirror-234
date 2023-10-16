# Simple

You could simply define parameters by listing all parameters in `parameters` list:

```python
from alphaz.utils.api import route, api, Parameter

@route("books", parameters=["name"])
def method_name():
    return "Book name is %s or %s"%(api["name"], api.get("name",default=""))
```

Parameter value is accessed by `api` instance, using `get` method, they could also be accessed using `get_parameters` method from `api` instance.

# Object

Or you could use the `Parameter` class to specify properties such as:

- **ptype**: value type int, str, bool, `SqlAlchemy model`
  - parameter is `automatically converted` to the specified type
  - if conversion failed an `exception` is raised
- **required**: the parameter is required or not
- **default**: default parameter value
- **options**: authorized values
- **mode**: input mode
- **cacheable**: parameter is taken into acount in the caching system or not
- **private**: parameter is hiden from documentation or not

```python
@route("/logs",
    parameters = [
        Parameter('page',required=True,ptype=int),
        Parameter('startDate',required=True),
        Parameter('endDate',default=None),
        Parameter('error', options=["Y","N"])
    ])
def admin_logs():
    return get_logs(**api.get_parameters())
```

> Promote this method as it allows a better control on parameters

# Default parameters

Some parameter are always available:
- **no_log** (bool): disable logs for this route
- **reset_cache** (bool): reset cache before calling this route
- **requester** (str): requester to this route
- **format** (str): output format
    - json: 
    - xml:
- **admin** (str): admin password
- **admin_user_id** (int): id of the user to connect has an admin 
