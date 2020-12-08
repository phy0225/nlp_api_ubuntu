#! python 3
# -*- coding:utf-8 -*-

from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from stat_freq import build_test_data_from_crf
from cut_freq import build_test_data_from_crf_cut

app = Flask(__name__)
api = Api(app)


class freq(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('content', type=str)
        content = parser.parse_args()['content']
        freq_result = build_test_data_from_crf(content)
        freq_result_dic = {}
        result = {}
        result_n = []
        result_v = []
        result_adj = []
        result_symptom = []
        for i in freq_result:
            for word,count in i.items():
                freq_result_dic[word] = count
        
        for word,count in freq_result_dic.items():
            if word == '':
                pass
            else:
                a = build_test_data_from_crf_cut(word)
                type =a[0]['type']
                if type == 'n':
                    result_n.append({'word':word,'count':count})
                    
                elif type == 'adj':
                    result_adj.append({'word':word,'count':count})
                
                elif type == 'v':
                    result_v.append({'word':word,'count':count})
                    
                elif type == 'symptom':
                    result_symptom.append({'word':word,'count':count})
                    
        result['n'] = result_n
        result['v'] = result_v
        result['adj'] = result_adj
        result['symptom'] = result_symptom
        
        return result


api.add_resource(freq, '/freq')


if __name__ == '__main__':
    app.run(port=5556,debug=True)