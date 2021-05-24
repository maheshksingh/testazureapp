from flask import Flask
from flask import render_template, abort, url_for, json, jsonify, Flask, Response, send_from_directory, send_file, Flask, make_response, request
import pandas as pd
import json
import os
import requests

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("public/form.html")
