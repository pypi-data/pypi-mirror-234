
![Build Status](https://drone-ext.mcos.nc/api/badges/scrippy/scrippy-db/status.svg) ![License](https://img.shields.io/static/v1?label=license&color=orange&message=MIT) ![Language](https://img.shields.io/static/v1?label=language&color=informational&message=Python)

![Scrippy, my scrangourou friend](./scrippy-db.png "Scrippy, my scrangourou friend")

# `scrippy_db`

Generic database client for the [`Scrippy`](https://codeberg.org/scrippy) framework.

## Requirements

### Python modules

#### List of required modules

The modules listed below will be installed automatically.

- psycopg2-binary
- cx-Oracle
- mysqlclient

## Installation

### Manual

```bash
git clone https://codeberg.org/scrippy/scrippy-db.git
cd scrippy-db
python -m pip install -r requirements.txt
make install
```

### With `pip`

```bash
pip install scrippy-db
```

### Usage

The `scrippy_db.db` module provides the `Db` object, which is intended to offer database usage functionality.

Connection to a database can be done either by directly providing connection parameters (`username`, `host`, `database`, `port`, `password`) to the constructor, or by providing the name of the _service_ to connect to.

The `db_type` parameter allows you to specify the type of database (`postgres`, `oracle`, or `mysql`). The default value of this parameter is `postgres`.

Query execution is performed with the `Db.execute()` method, which accepts the following parameters:
- `request`: The query itself (required)
- `params`: The query parameters in the exact order of appearance within the query (optional)
- `verbose`: Boolean indicating whether the query and its result should appear in the log. The log level must be set to at least `debug`.

A query may contain one or more variable parameters requiring the query to be adapted to these parameters.

For security reasons, some practices are **strictly** to be avoided, while others must be applied imperatively.

The parameters of a query must be passed in a *tuple* to the `Db.execute()` method, which will check the validity of your parameters.

Never **try** to manage the interpolation of parameters inside the query yourself.

#### Example

Data retrieval and conditional update of the database.

```python
from scrippy_db import db

db_user = "harry.fink"
db_password = "dead_parrot"
db_host = "flying.circus"
db_port = "5432"
db_base = "monty_python"
db_type = "postgres"

app_name = "spanish_inquisition"
app_version = "0.42.0"
app_status = "Deployed"
date = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')

with db.Db(username=db_user,
           host=db_host,
           port=db_port,
           database=db_base,
           password=db_password,
           db_type=db_type) as database:
  # Check application status
  req = """select app_status, app_version, date
            from apps
            where app_name=%s;"""
  params = (app_name, )
  current_status = database.execute(req, params, verbose=True)
  if current_status != None:
    # The application is already registered, we display its current status
    # We update its status
    params = {"app_name": app_name,
              "app_version": app_version,
              "app_status": app_status,
              "date": datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')}
    req = """insert into apps
                (app_name, app_version, app_status, date)
                values (%(app_name)s, %(app_version)s, %(app_status)s, %(date)s);"""
    result = database.execute(req, params, verbose=True)
  else:
    # The application has never been registered, we register the application and its status.
    req = """insert into apps
            (app_name, app_version, app_status, date)
            values (%(app_name)s, %(app_version)s, %(app_status)s, %(date)s);"""
    params = (app_name, app_version, app_status, date)
    result = database.execute(req, params)
```
