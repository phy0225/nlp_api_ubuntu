# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 09:38:13 2017

@author: 01055226
"""

from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from classifier_text import  text_classifier


app = Flask(__name__)
api = Api(app)

class classifier(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('content', type=str)
        content = parser.parse_args()['content']

        try:
            
            #print(result)
            #return jsonify({'state': '0'})
            result = text_classifier(content)
            return result
        except:
            return jsonify({'state': '1'})
        
        
        
    
    
api.add_resource(classifier,'/classifier')

if __name__ == '__main__':
    app.run(port=5599,debug=True)