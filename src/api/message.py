from flask import Flask, request
import flask
from src.handler import message

app = flask.Blueprint("api_message", __name__)

@app.route("/message", methods = ['GET'])
def get_message():
    senderid = request.args.get('sender')
    pageid = request.args.get('fanpage')
    page = request.args.get('page', 1)
    result = message.getMessage(senderid, pageid, page)
    return result, 200