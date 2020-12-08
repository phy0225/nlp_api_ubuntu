#! python 3
# -*- coding:utf-8 -*-

from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from ltp_parser import parse
from ltp_parser import segmentor_tag

app = Flask(__name__)
api = Api(app)

class parser_ltp(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('content', type=str)
        content = parser.parse_args()['content']
        return parse(content)

class segmentor(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('content', type=str)
        content = parser.parse_args()['content']
        words_list, tags_list, symptom_flag_list = segmentor_tag(content)
        segment_result = []
        id = 1
        for word,tag,symptom_flag in zip(words_list,tags_list,symptom_flag_list):
            a = {}
            a['id'] = id
            a['word'] = word
            a ['tag'] = tag
            a['symptom_flag'] = symptom_flag
            segment_result.append(a)
            id += 1
        return segment_result


api.add_resource(parser_ltp, '/parser')
api.add_resource(segmentor,'/segmentor')

if __name__ == '__main__':
    app.run(port=5555,debug=True)