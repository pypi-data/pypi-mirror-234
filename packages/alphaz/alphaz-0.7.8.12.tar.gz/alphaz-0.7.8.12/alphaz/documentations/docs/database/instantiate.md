This enable the use of model columns which is not possible using SqlAlchemy:

```py
attr = {
    Duck.name: name,
    Duck.duck_type_id: duck_type_id,
}
duck = Duck()
duck.init(attr)
```

or

```py
duck = Duck()
duck.init({
    Duck.name: name,
    Duck.duck_type_id: duck_type_id,
})
```

Instead of:

```py
attr = {
    Duck.name: name,
    Duck.duck_type_id: duck_type_id,
}
duck = Duck()
duck.init(**{x.key:y for x,y in attr.items()})
```