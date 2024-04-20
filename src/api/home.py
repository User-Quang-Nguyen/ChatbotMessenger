from flask import Flask
import flask

app = flask.Blueprint("api_home", __name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return "Home"