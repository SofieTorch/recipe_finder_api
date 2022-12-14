from flask import Response
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    pass

if __name__ == '__main__' :
    app.run(host='0.0.0.0', port='9000', debug=True)