import logging

from config import check_env_vars, config
from stuf.stuf_0204 import get_Lv01

from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)


def create_app():
    log = logging.getLogger(__name__)
    log_handler = logging.StreamHandler()
    app.logger.addHandler(log_handler)
    CORS(app)
    return app


@app.route('/brp_brandweer/<string:bag_id>', methods=['GET'])
def get_bag_id_info(bag_id):
    info = get_Lv01(bag_id, config)[0]
    response = jsonify(info)
    response.status_code = 404 if info.get("error") else 200
    return response


if __name__ == "__main__":
    check_env_vars()
    create_app().run()
