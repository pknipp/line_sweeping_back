import os
import json
from flask import Flask, render_template, request, session, redirect
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect, generate_csrf
from line_sweeping.config import Config
from datetime import datetime
from . import find_one


app = Flask(__name__)
app.config.from_object(Config)


# Application Security
CORS(app)


@app.after_request
def inject_csrf_token(response):
    response.set_cookie(
        'csrf_token',
        generate_csrf(),
        secure=True if os.environ.get('FLASK_ENV') else False,
        samesite='Strict' if os.environ.get('FLASK_ENV') else None,
        httponly=True)
    return response


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def react_root(path):
    print("path", path)
    if path == 'favicon.ico':
        return app.send_static_file('favicon.ico')
    return app.send_static_file('index.html')


@app.route('/')
def hello():
    return {"message": "Hello from line-sweeping back-end"}

@app.route('/<params>')
def index(params):
    params_dict = json.loads(params)
    n = params_dict["n"]
    fac = params_dict["fac"]
    iter = params_dict["iter"]
    distance_min = params_dict["distanceMin"]
    memo = params_dict["memo"]
    xys = params_dict["xys"]
    inter_town_distances = params_dict["interTownDistances"]
    response = find_one.find_one(n, fac, iter, distance_min, memo, xys, inter_town_distances)
    return response
