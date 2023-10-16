# Automatic structure

Compared to native SqlAlchemy in alpha you only need to instantiate the table model:

```py
from alphaz.models.database.models import AlphaTable, AlphaColumn, Text, integer
from core import DB

class DuckType(DB.Model, AlphaTable):
    __bind_key__ = DB
    __tablename__= "duck_type"

    type_id = AlphaColumn(Integer, primary_key=True, autoincrement=True)
    name = AlphaColumn(Text,nullable = False, default = "SuperDuck")

class DuckMedal(DB.Model, AlphaTable):
    __bind_key__ = DB
    __tablename__= "duck_medal"

    name = AlphaColumn(Text,nullable = False, default = "Lucky")
    duck_id       = AlphaColumn(Integer, ForeignKey ('duck.duck_id'      ), nullable     = False, default= -1)

class Duck(DB.Model, AlphaTable):
    __bind_key__ = DB
    __tablename__= "duck"

    duck_id = AlphaColumn(Integer, primary_key=True, autoincrement=True, visible=False)
    name = AlphaColumn(Text,nullable = False, default = "")

    # Many to one
    duck_type_id = AlphaColumn(Integer, ForeignKey ('duck_type.type_id'), nullable = False, default = -1, visible=False)
    duck_type = relationship("DuckType")

    # One to many
    medals = relationship("DuckMedals")
```

By default a select query on **Duck** class defined like this:

```py
master_duck = DuckType(ame="Master Duck")
DB.add(master_duck)

ducky = Duck(name="Ducky",duck_type=master_duck)
DB.add(ducky)

honnor_medal = DuckMedal(name="Honnor",duck_id=ducky.duck_id)
lucky_medal = DuckMedal(name="Lucky",duck_id=ducky.duck_id)
DB.add(ducky)

ducks = DB.select(Duck, filters=[Duck.name=="Ducky"], first=True)
```

Will result in this:

```json
{
  "duck_id": 1,
  "name": "Ducky",
  "duck_type": {
    "type_id": 1,
    "duck_type": "Master Duck"
  },
  "medals": [{ "name": "Honnor" }, { "name": "Lucky" }]
}
```


