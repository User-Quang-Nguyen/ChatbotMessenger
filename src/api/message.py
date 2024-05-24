from flask import Flask, request
import flask
from src.handler import message

app = flask.Blueprint("api_message", __name__)

@app.route("/message", methods=["GET"])
def get_messages():
    sender_id = request.args.get("sender")
    fanpage_id = request.args.get("fanpage")
    page_num = request.args.get("page", 1)
    result = message.get_messages_for_page(sender_id, fanpage_id, page_num)
    return result, 200
