# -*- coding:utf-8 -*-

from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from text_similar import cal_similarity


app = Flask(__name__)
api = Api(app)


class text_similar(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('content1', type=str)
        parser.add_argument('content2', type=str)
        parser.add_argument('type', type=int)
        
        content1 = parser.parse_args()['content1']
        content2 = parser.parse_args()['content2']
        type = parser.parse_args()['type']
        
        result = cal_similarity(content1,content2,type)
        return result

# type = 8 -- 计算短文本相似度
# type = 9 -- 计算语义相似度

api.add_resource(text_similar, '/text_similar')


if __name__ == '__main__':
    app.run(port=5559,debug=True)