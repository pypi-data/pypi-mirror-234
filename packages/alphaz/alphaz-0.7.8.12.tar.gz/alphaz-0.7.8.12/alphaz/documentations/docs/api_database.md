# Update

Alphaz include a special update method that simplifies updates via api routes

## Model as a parameter

!!! warning
This is not recommanded because you could not specified if a field of **Duck** is required or not

```py
@route(
    path='duck',
    methods=["PUT"],
    parameters=[
        Parameter("duck", ptype=Duck, required=True)
    ],
)
def update_duck():
    return DB.update(api["duck"])
```

## Route parameters to model

```py
@route(
    path='duck',
    methods=["PUT"],
    parameters=[
        Parameter("name", ptype=str, required=True),
        Parameter("duck_type_id", ptype=int)
    ],
)
def update_duck():
    return DB.update(Duck(**api.get_parameters()), not_none=True) # not_none is to set if you dont want None values to update fields
```

or using a function:

```py
def update_duck(name:str, duck_type_id:str):
    return DB.update(Duck(**locals()))

@route(
    path='duck',
    methods=["PUT"],
    parameters=[
        Parameter("name", ptype=str, required=True),
        Parameter("duck_type_id", ptype=int)
    ],
)
def update_duck():
    return update_duck(**api.get_parameters())
```