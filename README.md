##Flask-SQLAlchemySession

Provides an SQLAlchemy scoped session that creates
unique sessions per Flask request, following the guidelines documented at
[Using Custom Created Scopes](http://docs.sqlalchemy.org/en/rel_0_9/orm/contextual.html#using-custom-created-scopes).

[Documentation ![Documentation Status](https://readthedocs.org/projects/flask-sqlalchemy-session/badge/?version=latest)](http://flask-sqlalchemy-session.readthedocs.org/en/latest/)

###Usage

Initialize a `flask_scoped_session` as you would a
`scoped_session`, with the addition of a Flask
app. Then use the resulting session to query models:

```python
from flask import Flask, abort, jsonify
from flask_sqlalchemy_session import flask_scoped_session

app = Flask(__name__)
session = flask_scoped_session(session_factory, app)

@app.route("/users/<int:user_id>")
def user(user_id):
    user = session.query(User).get(user_id)
    if user is None:
        abort(404)
    return flask.jsonify(**user.to_dict())
```

The `current_session` is also provided as a convenient accessor to the session
of the current request, in the same spirit of `flask.request` and
`flask.current_app`.

```python
from flask_sqlalchemy_session import current_session

@app.route("/users/<int:user_id>")
def user(user_id):
    user = current_session.query(User).get(user_id)
    if user is None:
        abort(404)
    return flask.jsonify(**user.to_dict())
```
