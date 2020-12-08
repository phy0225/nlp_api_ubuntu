# -*- coding: utf-8 -*-

from flask import Flask,jsonify
from flask_restful import reqparse, Api, Resource
from nlpir_entity import nlpir

app = Flask(__name__)
api = Api(app)

class entity(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('content',type=str,required=True)
        args = parser.parse_args()
        
        try:
            sset = nlpir(args['content'])
            result_list = []
            for disease, couple in sset.items():
                single_dic = {}
                single_dic['disease'] = disease
                single_dic['symptom'], single_dic['symptomAll'] = couple[0], couple[1]
                result_list.append(single_dic)
            return result_list
        except:
            return jsonify({'message':'unknown error'})

api.add_resource(entity,'/entity')

if __name__ == '__main__':
    app.run(debug=True,port=5560)
