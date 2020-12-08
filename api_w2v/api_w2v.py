#! python 3
# -*- coding:utf-8 -*-

from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from w2v import word2vec_str
import simplejson as json


app = Flask(__name__)
api = Api(app)



class w2v(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('content', type=str)
        content = parser.parse_args()['content']
        result = word2vec_str(content)
        result_list = []
        for i, j in result.items():
            for word, value in j.items():
                single_dic = {}
                single_dic['word'] = word
                single_dic['value'] = value
            result_list.append(single_dic)
        return jsonify(result_list)


api.add_resource(w2v, '/w2v')


if __name__ == '__main__':
    app.run(port=5557,debug=True)