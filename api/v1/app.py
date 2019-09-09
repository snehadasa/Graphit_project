#!/usr/bin/python3
"""script that starts a Flask web application"""


from flask import Flask, render_template
from models import storage
from api.v1.views import app_views
from flask import Blueprint
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def app_teardown(self):
    """remove the current SQLAlchemy Session"""
    storage.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=5000,
            threaded=True)
