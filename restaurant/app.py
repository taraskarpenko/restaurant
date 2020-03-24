import os
from flask import Flask, Response, Request
app = Flask(__name__)

FLASK_RUN_PORT = int(os.getenv('FLASK_RUN_PORT', '3001'))

@app.route('/ping', methods=['GET'])
def ping():
    return Response(str({'success':True}), 200, mimetype='application/json')

if __name__ == '__main__':
    app.run(port=FLASK_RUN_PORT)