# -*- coding: utf-8 -*-
"""
Flask-SQLAlchemy-Session
-----------------------

Provides an SQLAlchemy scoped session that creates
unique sessions per Flask request
"""
# pylint: disable=invalid-name
from werkzeug.local import LocalProxy
from flask import current_app
from sqlalchemy.orm import scoped_session

__all__ = ["current_session", "flask_scoped_session"]
__version__ = 1.1


def _get_session():
    # pylint: disable=missing-docstring, protected-access
    app = current_app._get_current_object()
    if not hasattr(app, "scoped_session"):
        raise AttributeError(
            "{0} has no 'scoped_session' attribute. You need to initialize it "
            "with a flask_scoped_session.".format(app))
    return app.scoped_session


current_session = LocalProxy(_get_session)
"""Provides the current SQL Alchemy session within a request.

Will raise an exception if no :data:`~flask.current_app` is available or it has
not been initialized with a :class:`flask_scoped_session`
"""


class flask_scoped_session(scoped_session):
    """A :class:`~sqlalchemy.orm.scoping.scoped_session` whose scope is set to
    the Flask application context.
    """
    def __init__(self, session_factory, app=None):
        """
        :param session_factory: A callable that returns a
            :class:`~sqlalchemy.orm.session.Session`
        :param app: a :class:`~flask.Flask` application
        """
        super(flask_scoped_session, self).__init__(
            session_factory,
            scopefunc=_app_ctx_stack.__ident_func__)
        # the _app_ctx_stack.__ident_func__ is the greenlet.get_current, or
        # thread.get_ident if no greenlets are used.
        # each Flask request is launched in a seperate greenlet/thread, so our
        # session is unique per request
        # _app_ctx_stack looks like internal API but is the only way to get to
        # the active application context without adding logic to figure out
        # whether threads, greenlets, or something else is used to create new
        # application contexts. Keep in mind to refactor if Flask changes its
        # public/private API towards this.
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Setup scoped session creation and teardown for the passed ``app``.

        :param app: a :class:`~flask.Flask` application
        """
        app.scoped_session = self

        @app.teardown_appcontext
        def remove_scoped_session(*args, **kwargs):
            # pylint: disable=missing-docstring,unused-argument,unused-variable
            app.scoped_session.remove()
