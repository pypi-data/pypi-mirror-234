Methods are specified the same way as in `Flask`, using `methods` parameter:

```python
@route('logs', methods=["GET"])
def get_logs():
    return db.select(Logs)

@route('logs', methods=["POST"])
def set_logs():
    return db.add(Logs)
```

Methods can be managed using `different routes` or within `a single route`:

```python
@route('logs', methods=["GET", "POST", "DELETE"])
def get_logs():
    if api.is_get():
        return db.select(Logs)
    elif api.is_post():
        return db.add(Logs)
    elif api.is_delete():
        return db.delete(Logs)
```