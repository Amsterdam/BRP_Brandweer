import logging

from config import check_env_vars, config
from stuf.stuf_0204 import get_Lv01

from flask import Flask, jsonify
from flask_cors import CORS

log = logging.getLogger(__name__)

app = Flask(__name__)
log_handler = logging.StreamHandler()
app.logger.addHandler(log_handler)

CORS(app)


@app.route('/brp_brandweer/<string:bag_id>', methods=['GET'])
def get_bag_id_info(bag_id):
    return jsonify(get_Lv01(bag_id, config)[0])


if __name__ == "__main__":
    # execute only if run as a script
    # import pprint
    # from stuf.parse_0204 import _get_age, _get_age_category, _get_indicatoren
    #
    # pp = pprint.PrettyPrinter(indent=4)
    #
    # check_env_vars()
    #
    # birthdate = datetime.date(1962, 1, 17)
    # pp.pprint(_get_age(birthdate))
    # pp.pprint(_get_age_category(_get_age(birthdate)))
    # for i in [11, 12, 13, 69, 70, 71, -1, 999999]:
    #     print(i, _get_age_category(i))
    # pp.pprint((_get_indicatoren([])))
    # pp.pprint((_get_indicatoren([13])))
    # pp.pprint((_get_indicatoren([69])))
    # pp.pprint((_get_indicatoren([13, 69])))
    # pp.pprint((_get_indicatoren([12])))
    # pp.pprint((_get_indicatoren([70])))
    # pp.pprint((_get_indicatoren([12, 70])))
    # pp.pprint((_get_indicatoren(range(9))))
    # pp.pprint((_get_indicatoren(range(10))))
    #
    # pp.pprint(get_Lv01("0363200000399540", config))
    # pp.pprint(get_Lv01(["0363200000399540", "0363200000400471"], config))
    # pp.pprint(get_Lv01("0363200000399540x", config))

    check_env_vars()

    app.run()

