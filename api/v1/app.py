#!/usr/bin/python3
"""script that starts a Flask web application"""


from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask import Blueprint
app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def page_not_found(e):
    """Error handling, 404"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def app_teardown(self):
    """remove the current SQLAlchemy Session"""
    storage.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=5000,
            threaded=True)
