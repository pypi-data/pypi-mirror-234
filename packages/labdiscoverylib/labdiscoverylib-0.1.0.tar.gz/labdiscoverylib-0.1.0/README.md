# labdiscoverylib

[![CircleCI](https://circleci.com/gh/labsland/labdiscoverylib.svg?style=svg)](https://circleci.com/gh/labsland/labdiscoverylib)
[![documentation](https://raw.githubusercontent.com/labsland/labdiscoverylib/0.5.x/docs/source/_static/docs.svg)](https://developers.labsland.com/labdiscoverylib/)
[![Version](https://img.shields.io/pypi/v/labdiscoverylib.svg)](https://pypi.python.org/pypi/labdiscoverylib/)
[![Python versions](https://img.shields.io/pypi/pyversions/labdiscoverylib.svg)](https://pypi.python.org/pypi/labdiscoverylib/)

**labdiscoverylib** is a library for creating [LabDiscoveryEngine](https://github.com/labsland/labdiscoveryengine/) remote laboratories, based on [weblablib](https://developers.labsland.com/weblablib).

A remote laboratory is a software and hardware system that enables students to access real laboratories through the Internet.
For example, a student can be learning how to program a robot by writing code in a computer at home and sending it to a remote laboratory, where the student can see how the program behaves in a real environment.

Creating a remote laboratory may imply many layers, such as authentication, authorization, scheduling, etc., so Remote Laboratory Management Systems (RLMS) were created to make the common layers of remote laboatories.
WebLab-Deusto is an Open Source RLMS, and it has multiple ways ([see the docs](https://weblabdeusto.readthedocs.org)) to create a remote laboratory (in different programming languages, etc.).

In the case of Python, with the popular [Flask](http://flask.pocoo.org) microframework, **labdiscoverylib** is the wrapper used to create *unmanaged labs*.
*Unmanaged labs* is a term used in WebLab-Deusto to refer laboratories where the authors develop the full stack (server, client, deployment), as opposed to *managed labs*.

If you are familiar with Flask and with Web development, and want to be able to customize everything but not need to implement all the layers of authentication, administration, etc., this library would be very useful. Furthermore, this library allows you to develop remote laboratories for many environments (from regular computers with Linux to systems such as Raspberry Pi). And it integrates very well with other Flask components such as [Flask-SocketIO](https://flask-socketio.readthedocs.io/), [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/) for databases or [Flask-Assets](https://flask-assets.readthedocs.io/).

## Documentation

Read the documentation: https://developers.labsland.com/labdiscoverylib/

## Installation

Simply use pip:
```
  pip install labdiscoverylib
```

## Simple usage

```python
from flask import Flask, url_for
from labdiscoverylib import WebLab, weblab_user, requires_active

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'secret', # MUST CHANGE
    'WEBLAB_USERNAME': 'weblabdeusto',
    'WEBLAB_PASSWORD': 'password',
})

weblab = WebLab(app)

@weblab.on_start
def on_start(client_data, server_data):
    # ...
    print("Starting user")

@weblab.on_dispose
def on_dispose():
    # ...
    print("Ending user")

@weblab.initial_url
def initial_url():
    return url_for('index')

@app.route('/')
@requires_active
def index():
    return "Hello, {}".format(weblab_user.username)

if __name__ == '__main__':
    app.run(debug=True)
```

## Advance examples

You may find [here](https://github.com/labsland/labdiscoverylib/tree/master/examples) the following examples:
 * [simple](https://github.com/labsland/labdiscoverylib/tree/master/examples/simple): basic usage, all in one file.
 * [advanced](https://github.com/labsland/labdiscoverylib/tree/master/examples/advanced): more advanced usage, with separation of files, tasks, more complex session management
 * [complete](https://github.com/labsland/labdiscoverylib/tree/master/examples/complete): based on advanced, but using WebSockets with Flask-SocketIO, internationalization with Flask-Babel and minimified static files with Flask-Assets.

There is another example called ``quickstart``, which is the one used in the documentation, which is something in between ``simple`` and ``advanced``.
