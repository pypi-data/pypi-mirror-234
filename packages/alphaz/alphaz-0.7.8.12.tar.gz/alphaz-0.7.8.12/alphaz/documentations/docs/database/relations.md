```py
    return DB.select(
        Duck,
        filters=[Duck.duck_type.has(DuckType.name.like(name))]
    )
```

Will produce a query like:

```sql
SELECT * FROM DUCK WHERE EXISTS (SELECT 1 FROM DUCKTYPE where DUCKTYPE.id==DUCK.ducktype_id and DUCKTYPE.name=name)
```

[Doc](https://www.kite.com/python/docs/sqlalchemy.orm.properties.RelationshipProperty.Comparator.has)