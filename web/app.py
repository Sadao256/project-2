"""
John Doe's Flask API.
"""

import os
import configparser
from flask import Flask, abort, send_from_directory

app = Flask(__name__)

@app.route("/")
def index():
    return "UOCIS docker demo!\n"

@app.route("/<string:file>")
def hello(file):
    if (".." in file) or ("~" in file):
        #abort(403)
        return send_from_directory("pages/", "403.html"), 403 

    try:
        return send_from_directory("pages/", file), 200
    except:
        #abort(404)
        return send_from_directory("pages/", "404.html"), 404

@app.errorhandler(403)
def forbidden(error):
    return send_from_directory("pages/", "403.html"), 403

@app.errorhandler(404)
def not_found(error):
    return send_from_directory("pages/", "404.html"), 404

def parse_config(config_paths):
    config_path = None
    for f in config_paths:
        if os.path.isfile(f):
            config_path = f
            break

    if config_path is None:
        raise RuntimeError("Configuration file not found!")

    config = configparser.ConfigParser()
    config.read(config_path)
    return config

config = parse_config(["credentials.ini", "default.ini"])
debug_value = config["SERVER"]["DEBUG"]
port = config["SERVER"]["PORT"]


if __name__ == "__main__":
    app.run(debug=debug_value, host='0.0.0.0', port = port)
