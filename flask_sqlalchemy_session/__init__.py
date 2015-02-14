# -*- coding: utf-8 -*-
from werkzeug.local import LocalProxy
from flask import _app_ctx_stack, current_app
from sqlalchemy.orm import scoped_session


__all__ = ["current_session", "flask_scoped_session"]


def _get_session():
    context = _app_ctx_stack.top
    if context is None:
        raise RuntimeError(
            "Cannot access current_session when outside of an application "
            "context.")
    app = current_app._get_current_object()
    if not hasattr(app, "scoped_session"):
        raise AttributeError(
            "{} has no 'scoped_session' attribute. You need to initialize it "
            "with a flask_scoped_session.".format(app))
    return app.scoped_session


current_session = LocalProxy(_get_session)
"""Provides the current SQL Alchemy session within a request."""


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
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Setup scoped sesssion creation and teardown for the passed ``app``.

        :param app: a :class:`~flask.Flask` application
        """
        app.scoped_session = self

        @app.teardown_appcontext
        def remove_scoped_session(*args, **kwargs):
            app.scoped_session.remove()
