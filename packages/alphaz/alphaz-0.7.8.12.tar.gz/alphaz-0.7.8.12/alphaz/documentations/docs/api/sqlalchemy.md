If you specify a `SqlAlchemy model` as a type it will be automatically converted to the specified model.

```python
from core import core
db = core.db

class Logs(db.Model, AlphaTable):
    __tablename__ = 'LOGS'

    id                       = AlphaColumn(Integer,nullable=False,primary_key=True)
    name                     = AlphaColumn(String,nullable=False)

@route("logs",
    parameters = [
        Parameter('log',ptype=Logs)
    ])
def admin_logs():
    db.add(api['log'])
```