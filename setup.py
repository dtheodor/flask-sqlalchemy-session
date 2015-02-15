"""
Flask-SQLAlchemySession
-----------------------

Provides an SQL Alchemy scoped session that will create unique sessions per
Flask request.

http://docs.sqlalchemy.org/en/rel_0_9/orm/contextual.html#using-custom-created-scopes
"""
from setuptools import setup

setup(name="Flask-SQLAlchemySession",
      version="1.0",
      packages=["flask_sqlalchemy_session"],
      author="Dimitris Theodorou",
      url='http://github/dtheodor/flask-sqlalchemy-session',
      description='SQL Alchemy session scoped on Flask requests',
      long_description=__doc__,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Environment :: Web Environment',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      install_requires=["sqlalchemy>=0.9", "Flask>=0.9", "Werkzeug>=0.6.1"],
      tests_require=["pytest>=2.6", "mock>=1.0"],
      extras_require={
          'docs': ["Sphinx>=1.2.3", "alabaster>=0.6.3"]
      }
)
