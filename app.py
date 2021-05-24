from flask import Flask
import pandas as pd
import json
import os
import requests

app = Flask(__name__)

@app.route("/")
def hello():
    return "Yo, you the man"
