#### Select query

```python
    duck = Duck.query.filter_by(name=name).first()
    duck.duck_type_id = duck_type_id
    db.session.commit()
```

#### Init

```py
    new_duck = Duck("name": name, "duck_type_id": duck_type_id)
    db.session.merge(new_duck)
    db.session.commit()
```

or

```py
    attr = {
        "name": name,
        "duck_type_id": duck_type_id,
    }
    duck = Duck(**attr)
    db.session.merge(new_duck)
    db.session.commit()
```

#### Init and update

```py
new_duck = Duck()
new_duck.name = name
new_duck.duck_type_id = duck_type_id
db.session.merge(new_duck)
db.session.commit()
```
