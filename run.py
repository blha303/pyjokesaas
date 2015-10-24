from flask import Flask, request, jsonify
import pyjokes

app = Flask(__name__)
app.debug = True

# http://flask.pocoo.org/snippets/45/
def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']

def _joke():
    return pyjokes.get_joke(language=request.args.get("language", "en"), category=request.args.get("category", "neutral"))

def _jokes():
    return pyjokes.get_jokes(language=request.args.get("language", "en"), category=request.args.get("category", "neutral"))

@app.route("/get_joke")
def get_joke():
    if request_wants_json():
        return jsonify({"joke": _joke()})
    return _joke()

@app.route("/get_jokes")
def get_jokes():
    return "<ul>\n" + "\n".join("<li>{}</li>".format(j) for j in _jokes()) + "</ul>\n"

@app.route("/")
def index():
    return """<h1>Pyjokes As A Service</h1>
Methods: <strong>/get_jokes</strong>, <strong>/get_joke</strong><br>
Parameters:
<dt>language</dt>
<dd>choices: neutral, adult, chuck, all</dd>
<dt>category</dt>
<dd>choices: en, de, es, gl</dd>"""

if __name__ == "__main__":
    app.run(port=45731)
