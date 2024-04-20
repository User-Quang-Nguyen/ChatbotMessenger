from src.api.home import app as api_home
from src.api.webhook import app as api_webhook
from src.config import args
from src.api_dto.api_exception import *
from flask import Flask

app = Flask(__name__)

app.register_error_handler(Exception, error_handler)
app.register_blueprint(api_home)
app.register_blueprint(api_webhook)

if __name__ == "__main__":
    app.run(host = args.get("service_host"), port = args.get("service_port"), debug = True)