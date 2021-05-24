from flask import Flask
from flask import render_template
import pandas as pd
import json
import os
import requests

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("public/form.html")
