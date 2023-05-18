
from flask import Flask, jsonify, render_template_string, request
import flask
from flask_cors import CORS
import requests
import pyfiglet  

app = Flask(__name__)
cors = CORS(app, origins=["https://chat.openai.com"])

@app.route('/text', methods=['POST'])
def convert_text_to_ascii():
    text = request.args.get('text', None)
    font = request.args.get('font', 'standard')

    if text is None:
        return jsonify({'status': 'error', 'message': 'No text provided'}), 400

    try:
        ascii_art = pyfiglet.figlet_format(text, font=font)
        return jsonify({
            'status': 'success',
            'text': text,
            'font': font,
            'ascii': ascii_art
        }), 200
    except pyfiglet.FontNotFound:
        return jsonify({'status': 'error', 'message': 'Font not found'}), 400
 
@app.route('/fonts', methods=['GET'])
def list_fonts():
    fonts = pyfiglet.FigletFont.getFonts()
    return jsonify(fonts), 200

@app.get("/logo.png")
def plugin_logo():
  filename = 'figlet1.png'
  return flask.send_file(filename, mimetype='image/png')



@app.get("/.well-known/ai-plugin.json")
def plugin_manifest():
  with open("./well-known/ai-plugin.json") as f:
    text = f.read()
    return flask.Response(text, mimetype="text/json")


@app.get("/openapi.yaml")
def openapi_spec():
  with open("openapi.yaml") as f:
    text = f.read()
    return flask.Response(text, mimetype="text/yaml")

if __name__ == '__main__':
    app.run(host='localhost', port=3000)
