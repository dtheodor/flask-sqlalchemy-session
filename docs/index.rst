=======================
Flask-SQLAlchemySession
=======================
.. toctree::
   :maxdepth: 2
.. currentmodule:: flask_sqlalchemy_session

Flask-SQLALchemySession is a tiny library providing an SQLAlchemy scoped
session that creates
unique sessions per Flask request, following the guidelines documented at
`Using Custom Created Scopes <http://docs.sqlalchemy.org/en/rel_0_9/orm/contextual.html#using-custom-created-scopes>`_.

.. contents::
   :local:
   :backlinks: none

Basic usage
-----------

Initialize a :class:`flask_scoped_session` as you would a
:class:`~sqlalchemy.orm.scoping.scoped_session`, with the addition of a Flask
app. Then use the resulting session to query models::

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



The :data:`current_session` is also provided as a convenient accessor to the session
of the current request, in the same spirit of :class:`~flask.request` and
:data:`~flask.current_app`.


Implementation
--------------
The :class:`flask_scoped_session` is a simple wrapper over the original
:class:`~sqlalchemy.orm.scoping.scoped_session` that sets the scope to the Flask
application context, using the right ``scopefunc`` parameter. The application
context is rougly equivalent to a Flask request (more
`here <http://flask.pocoo.org/docs/0.10/appcontext/>`_). The session is
destroyed on application context teardown.


Full Example
------------

This is a complete example with SQL Alchemy model and engine initialization,
followed by Flask app creation and querying of models within a Flask request.

Declare your models::

    from sqlalchemy import Column, Integer, String
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    class User(Base):
        id = Column(Integer, primary_key=True)
        name = Column(String)

        def to_dict(self):
            return {"id": self.id,
                    "name": self.name}

Initialize the database engine and session::

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine("sqlite://")
    session_factory = sessionmaker(bind=engine)

Instantiate a Flask application and query a model within a request::

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

Or use the equivalent :data:`current_session`::

    from flask_sqlalchemy_session import current_session

    @app.route("/users/<int:user_id>")
    def user(user_id):
        user = current_session.query(User).get(user_id)
        if user is None:
            abort(404)
        return flask.jsonify(**user.to_dict())



Comparison with Flask-SQLAlchemy
--------------------------------

The `Flask-SQLAlchemy <https://pythonhosted.org/Flask-SQLAlchemy/>`_ project
also provides a request-scoped session. It comes an API that
acts as a facade over various SQL Alchemy APIs (engines,
models, metadata). This API buries the
engine/session initialization behind the Flask app initialization, detracts
from the original by removing decisions, confuses a user
already familiar with SQL Alchemy, and tightly couples the data layer with the
Flask app.

Flask-SQLAlchemySession is not
intrusive to the original SQL Alchemy APIs in any way, and
does not force you to couple your data layer with your web application. It's
sole purpose is to enable request-scoped sessions on top of
your SQL Alchemy constructs. In my opinion, if you use
SQL Alchemy you should be using the original API and its accompanying
documentation and not be trying to juggle with multiple APIs and documentations
for the same purpose.


API
---

.. automodule:: flask_sqlalchemy_session

    .. data:: current_session

        Provides the current SQL Alchemy session within a request.

    .. autoclass:: flask_scoped_session
        :members:
        :special-members:


