"""Test scrippy_db."""
from scrippy_db import db

db_user = "postgres"
db_password = "postgres"
db_host = "scrippy_db"
db_port = "5432"
db_base = "scrippy"

user_id = 0
user_name = "FINK"
user_givenname = "Harry"
user_password = "D34D P4RR0T"


def test_pgsql_exec():
  """Test PostgresSQL connexion and request"""
  with db.Db(username=db_user, host=db_host, port=db_port, database=db_base, password=db_password) as database:
    req = "select id, name, givenname, password from users where id=%s;"
    params = (user_id,)
    user = database.execute(req, params, verbose=True)
    user = user[0]
    assert user is not None
    assert user[1] == user_name
    assert user[2] == user_givenname
    assert user[3] == user_password
