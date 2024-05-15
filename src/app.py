from flask import Flask, request, send_file, jsonify
import os
from tempfile import NamedTemporaryFile
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from sparkline import Sparkline

app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello World'


@app.route('/api/sparkline', methods=['POST'])
def sparkline():
    data = request.get_json()
    y_coord = data.get('y_coord')
    title = data.get('title', 'None')
    style = data.get('style', 'cyberpunk')

    if not y_coord:
        return jsonify({"error": "y_coord is required"}), 400

    sparkline = Sparkline(y_coord=y_coord, title=title, style=style)

    with NamedTemporaryFile(delete=True, suffix='.png') as temp_file:
        sparkline.create(temp_file.name)
        temp_file.seek(0)
        return send_file(temp_file.name, mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)