
!!! note
The associated Schema is created automatically, with classic and nested fields.

However Marshmallow schema could be defined using the classic way [Marshmallow](https://marshmallow.readthedocs.io/en/stable/index.html):

- Set visible to **False** if you dont want the column to appears in the Schema.

!!! important
Schema must be defined after the Model

```py
DB = core.db

class DuckTypeSchema(Schema):
    type_id = fields.Integer()
    name = fields.String()

class DuckMedalSchema(Schema):
    name = fields.String()

class DuckSchema(Schema):
    name = fields.String()

    # Many to One
    duck_type = fields.Nested(DuckTypeSchema)

    # One to many
    medals = fields.List(fields.Nested(DuckMedalSchema))
```

!!! important
**Alpha** will automatically detect the schema if the name is defined as `"{ModelName}Schema"` and is located in the same file.

!!! note
In this mode, Schema could be defined automatically, excepted for nested fields.

# Specific Schema

Schema could be specified for every request:

```py
DB.select(model  = Duck, schema = DuckSchema)
```