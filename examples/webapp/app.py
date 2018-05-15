#!/usr/bin/env python3

from flask import Flask, jsonify, make_response, request

from pseudol10nutil import PseudoL10nUtil

app = Flask(__name__)
appname = "pseudol10nutil"
api_version = "v1.0"
api_base_url = "/{0}/api/{1}/".format(appname, api_version)
util = PseudoL10nUtil()


@app.errorhandler(404)
def handle_404(error):
    return make_response(jsonify({"error": "404 Error: URL not found.  Please check your spelling and try again."}), 404)


@app.route(api_base_url + "pseudo", methods=["POST"])
def do_pseudo():
    if "strings" in request.get_json():
        data = request.json["strings"]
    else:
        return make_response(jsonify({"error": "400 Error: Could not process request."}), 400)
    for k, v in data.items():
        data[k] = util.pseudolocalize(v)
    result = {"strings": data}
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
