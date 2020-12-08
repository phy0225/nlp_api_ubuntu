# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from flask_restful import reqparse, Api, Resource
import requests

app = Flask(__name__)
api = Api(app)


class test(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('content', type=str)
        content = parser.parse_args()['content']

        return jsonify({'state': '1', 'content': content})


api.add_resource(test, '/test')


if __name__ == '__main__':
    app.run(debug=True, port=5555)
    

url_test = 'http://127.0.0.1:5555/test' 
params_test = {'content': '患者高血压和心脏病五年，我就觉得我有糖尿病'}
test = requests.post(url_test, params=params_test) 