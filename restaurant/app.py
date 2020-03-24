import os

from flask import Flask, Response

app = Flask(__name__)

FLASK_RUN_PORT = int(os.getenv('FLASK_RUN_PORT', '5000'))
FLASK_RUN_HOST = os.getenv('FLASK_RUN_HOST', '127.0.0.1')


@app.route('/ping', methods=['GET'])
def ping():
    return Response(str({'success': True}), 200, mimetype='application/json')


if __name__ == '__main__':
    app.run(host=FLASK_RUN_HOST, port=FLASK_RUN_PORT)
