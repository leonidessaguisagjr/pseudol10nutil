#!/usr/bin/env python3

from flask import Flask, jsonify, make_response, redirect, render_template, request

from pseudol10nutil import PseudoL10nUtil
import pseudol10nutil.transforms as xforms

app = Flask(__name__)
appname = "pseudol10nutil"
api_version = "v1.0"
api_base_url = "/{0}/api/{1}/".format(appname, api_version)
ui_base_url = "/{0}/".format(appname)
util = PseudoL10nUtil()


@app.errorhandler(404)
def handle_404(error):
    if request.accept_mimetypes.best_match(['application/json', 'text/html']) == 'application/json':
        return make_response(jsonify({"error": "404 Error: URL not found.  Please check your spelling and try again."}), 404)
    else:
        return render_template("404.html"), 404


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


@app.route("/")
def home():
    return redirect(ui_base_url)


@app.route(ui_base_url, methods=["GET", "POST"])
def do_pseudo_ui():
    if request.method == "POST":
        input_text = request.form.get("pseudolocalize_input")
        substitute = request.form.get("substitution_type")
        brackets = request.form.get("add_brackets")
        pad_length = True if "pad_length" in request.form else False

        transforms = []
        form_options = {}  # Preserve options on post back

        if substitute == "diacritics":
            transforms.append(xforms.transliterate_diacritic)
            form_options['sub_diacritics'] = 'checked'
        elif substitute == "fullwidth":
            transforms.append(xforms.transliterate_fullwidth)
            form_options['sub_fullwidth'] = 'checked'
        elif substitute == "circled":
            transforms.append(xforms.transliterate_circled)
            form_options['sub_circled'] = 'checked'
        else:
            form_options['sub_none'] = 'checked'

        if pad_length:
            transforms.append(xforms.pad_length)
            form_options['do_pad_length'] = 'checked'

        if brackets == "square":
            transforms.append(xforms.square_brackets)
            form_options['brackets_square'] = 'checked'
        elif brackets == "angle":
            transforms.append(xforms.angle_brackets)
            form_options['brackets_angle'] = 'checked'
        elif brackets == "curly":
            transforms.append(xforms.curly_brackets)
            form_options['brackets_curly'] = 'checked'
        else:
            form_options['brackets_none'] = 'checked'

        util.transforms = transforms
        pseudolocalized_text_output = util.pseudolocalize(input_text)
        return render_template("pseudolocalize_template.html",
                               pseudolocalized_text_input=input_text,
                               pseudolocalized_text_output=pseudolocalized_text_output,
                               **form_options)
    else:
        default_options = {
            'sub_diacritics': 'checked',
            'brackets_square':'checked',
            'do_pad_length': 'checked',
        }
        return render_template("pseudolocalize_template.html", **default_options)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
