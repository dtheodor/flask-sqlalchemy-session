# -*- coding: utf-8 -*-
from unittest import mock

import pytest
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from flask_sqlalchemy_session import flask_scoped_session, current_session


@pytest.fixture
def sqlite_engine():
    """Return an sqlite engine"""
    return create_engine("sqlite://")


@pytest.fixture
def flask_app():
    """Return a flask app with debug and testing on"""
    app = Flask(__name__)
    app.testing = True
    app.debug = True
    return app


@pytest.fixture
def unitialized_session(sqlite_engine):
    """Return a request_scoped_session that has not been used for a flask app"""
    ses = flask_scoped_session(sessionmaker(bind=sqlite_engine))
    _remove = ses.remove
    ses.remove = mock.Mock(side_effect=_remove)
    return ses


@pytest.fixture
def session(unitialized_session, flask_app):
    """Return a request_scoped_session initialized on the flask_app fixture"""
    unitialized_session.init_app(flask_app)
    return unitialized_session


def test_constructor(sqlite_engine, flask_app):
    """Test init_app is called when an app is passed in the constructor"""
    with mock.patch.object(flask_scoped_session, "init_app"):
        ses = flask_scoped_session(sessionmaker(bind=sqlite_engine), flask_app)
        ses.init_app.assert_called_once_with(flask_app)


def test_current_session_uninitialized_app(flask_app):
    """Test accessing current_session without initializing an app"""
    with flask_app.test_request_context():
        with pytest.raises(AttributeError):
            current_session()


class TestRequestScopedSession(object):
    """Test handling of the session in a flask request"""

    def test_session_same_request(self, flask_app, session):
        with flask_app.test_request_context():
            assert session.query
            assert isinstance(session(), Session)
            assert session() is session()

        assert session.remove.call_count == 1

    def test_session_different_request(self, flask_app, session):
        with flask_app.test_request_context():
            prev_id = id(session())

        with flask_app.test_request_context():
            assert prev_id != id(session())

        assert session.remove.call_count == 2


@pytest.mark.usefixtures("session")
class TestCurrentSession(object):
    """Test current_session"""

    def test_session_same_request(self, flask_app):
        with flask_app.test_request_context():
            assert current_session.query
            assert isinstance(current_session._get_current_object()(), Session)
            assert current_session._get_current_object()() is \
                   current_session._get_current_object()()

    def test_session_different_request(self, flask_app):
        with flask_app.test_request_context():
            prev_id = id(current_session._get_current_object()())

        with flask_app.test_request_context():
            assert prev_id != id(current_session._get_current_object()())
