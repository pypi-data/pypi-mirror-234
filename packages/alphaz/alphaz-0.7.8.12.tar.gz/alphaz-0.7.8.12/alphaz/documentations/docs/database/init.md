# Route

The route **database/init** could be use to init the database or some tables.

```py 
@route(
    "/database/init",
    admin=True,
    parameters=[
        Parameter("binds", ptype=list[str]),
        Parameter("tables", ptype=list[str]),
        Parameter("drop", ptype=bool, default=False),
        Parameter("truncate", ptype=bool, default=False),
        Parameter("force", ptype=bool, default=False),
        Parameter("create", ptype=bool, default=False),
    ],
)
```

# Configuration

Content of tables could be pre-defined in various ways:

- **python**: you have to specify the directory where the **py** files are defined using the **init_database_dir_py** parameter in your database configuration.

For every table you want to fill you could specify **objects** which are models in this situation:

```py
from models.database.olca import TblGroups

ini = {
    TblGroups: {
        "objects": [
            TblGroups.instantiate(
                2, "hidden", "far fa-eye-slash", "var(--ion-color-light)"
            ),
            TblGroups.instantiate(3, "steps", "fas fa-cogs", "var(--ion-color-danger)"),
            TblGroups.instantiate(
                4, "materials", "fas fa-cubes", "var(--ion-color-primary)"
            ),
            TblGroups.instantiate(
                5, "transports", "fas fa-dolly-flatbed", "var(--ion-color-secondary)"
            ),
            TblGroups.instantiate(
                6, "powers", "fas fa-lightbulb", "var(--ion-color-warning)"
            ),
        ]
    },
}
```

- **json**: you have to specify the directory where the **json** files are defined using the **init_database_dir_json** parameter in your database configuration.

```json
{
    "sophisme": {
        "headers": ["theme","sophisme","user","proposition"],
        "values":
            [
                [5,20,6,34],
                [5,7,1,35],
                [5,9,1,35]
            ]
    }
}
```

- **sql**: you have to specify the directory where the **sql** files are defined using the **init_database_dir_sql** parameter in your database configuration.

Here the code is directly executed, so it could have any valid sql structure.

```sql

```