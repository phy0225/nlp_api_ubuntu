# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from flask_restful import reqparse, Api, Resource
from nlpir_entity import nlpir
from stat_freq import build_test_data_from_crf
from cut_freq import build_test_data_from_crf_cut
from ltp_parser import parse
from ltp_parser import segmentor_tag
from mlstm_sentiment import predict_model
from text_similar import cal_similarity
from w2v import word2vec_str
from classifier_text import  text_classifier
import numpy as np


app = Flask(__name__)
api = Api(app)


class entity(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('content', type=str, required=True)
        args = parser.parse_args()
        try:
            sset = nlpir(args['content'])
            result_list = []
            for disease, couple in sset.items():
                single_dic = {}
                single_dic['disease'] = disease
                single_dic['symptom'], single_dic['symptomAll'] = couple[0], couple[1]
                result_list.append(single_dic)
            result = {
                    'code': 0,
                    'message': '',
                   } 
            result['data'] = result_list
            return result
        except:
            result = {
                    'code': 1,
                    'message': 'unknown error',
                   } 
            result['data'] = ''
            return result


class freq(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('content', type=str)
        parser.add_argument('tags', type=str, action='append')
        content = parser.parse_args()['content']
        tags = parser.parse_args()['tags']
        freq_result = build_test_data_from_crf(content)
        freq_result_dic = {}
        for i in freq_result:
            for word, count in i.items():
                freq_result_dic[word] = count
        cut_result = build_test_data_from_crf_cut(content)
        freq_result_dic = {}
        result = {}
        result_n = []
        result_v = []
        result_adj = []
        result_symptom = []
        result_vn = []
        for i in freq_result:
            for word, count in i.items():
                freq_result_dic[word] = count

        for word, count in freq_result_dic.items():
            if word == '':
                pass
            else:
                for i in cut_result:
                    if i['term'] == word:
                        type = i['type']
                        break
                if type == 'n':
                    result_n.append({'word': word, 'count': count})

                elif type == 'a':
                    result_adj.append({'word': word, 'count': count})

                elif type == 'v':
                    result_v.append({'word': word, 'count': count})

                elif type == 'symptom':
                    result_symptom.append({'word': word, 'count': count})
                
                elif type == 'vn':
                    result_vn.append({'word': word, 'count': count})

        result['n'] = result_n
        result['v'] = result_v
        result['a'] = result_adj
        result['symptom'] = result_symptom
        result['vn'] = result_vn
        
        #select top_num from each tag of word
        if len(result['n']) <= 40:
            pass
        else:
            result['n'] = sorted(result['n'], key=lambda item: item['count'], reverse=True)[:40]
        
        if len(result['v']) <= 20:
            pass
        else:
            result['v'] = sorted(result['v'], key=lambda item: item['count'], reverse=True)[:20]
        
        if len(result['a']) <= 20:
            pass
        else:
            result['a'] = sorted(result['a'], key=lambda item: item['count'], reverse=True)[:20]
        
        if len(result['symptom']) <= 20:
            pass
        else:
            result['symptom'] = sorted(result['symptom'], key=lambda item: item['count'], reverse=True)[:20]
        
        
        if len(result['vn']) <= 20:
            pass
        else:
            result['vn'] = sorted(result['vn'], key=lambda item: item['count'], reverse=True)[:20]
        
        result_selected = []
        for i in result:
            if i in tags:
                for j in result[i]:
                    j['tag'] = i
                    result_selected.append(j)
                    
        result_finally = {
                    'code': 0,
                    'message': '',
                   } 
        result_finally['data'] = result_selected
            
        return result_finally
        
#        freq_result_dic = {}
#        result = {}
#        result_n = []
#        result_v = []
#        result_adj = []
#        result_symptom = []
#        result_vn = []
#        for i in freq_result:
#            for word, count in i.items():
#                freq_result_dic[word] = count
#
#        for word, count in freq_result_dic.items():
#            if word == '':
#                pass
#            else:
#                a = build_test_data_from_crf_cut(word)
#                type = a[0]['type']
#                if type == 'n':
#                    result_n.append({'word': word, 'count': count})
#
#                elif type == 'adj':
#                    result_adj.append({'word': word, 'count': count})
#
#                elif type == 'v':
#                    result_v.append({'word': word, 'count': count})
#
#                elif type == 'symptom':
#                    result_symptom.append({'word': word, 'count': count})
#                
#                elif type == 'vn':
#                    result_vn.append({'word': word, 'count': count})
#
#        result['n'] = result_n
#        result['v'] = result_v
#        result['adj'] = result_adj
#        result['symptom'] = result_symptom
#        result['vn'] = result_vn
#        
#        #select top_num from each tag of word
#        if len(result['n']) <= 40:
#            pass
#        else:
#            result['n'] = sorted(result['n'], key=lambda item: item['count'], reverse=True)[:40]
#        
#        if len(result['v']) <= 20:
#            pass
#        else:
#            result['v'] = sorted(result['v'], key=lambda item: item['count'], reverse=True)[:20]
#        
#        if len(result['adj']) <= 20:
#            pass
#        else:
#            result['adj'] = sorted(result['adj'], key=lambda item: item['count'], reverse=True)[:20]
#        
#        if len(result['symptom']) <= 20:
#            pass
#        else:
#            result['symptom'] = sorted(result['symptom'], key=lambda item: item['count'], reverse=True)[:20]
#        
#        
#        if len(result['vn']) <= 20:
#            pass
#        else:
#            result['vn'] = sorted(result['vn'], key=lambda item: item['count'], reverse=True)[:20]
#        
#        result_selected = []
#        for i in result:
#            if i in tags:
#                for j in result[i]:
#                    j['tag'] = i
#                    result_selected.append(j)
#                    
#        result_finally = {
#                    'code': 0,
#                    'message': '',
#                   } a
#        result_finally['data'] = result_selected
#            
#        return result_finally
        

class parser_ltp(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('content', type=str)
        content = parser.parse_args()['content']
        if len('content') > 50:
            result = {
                    'code': 1,
                    'message': '依存句法分析句子长度超过50',
                    'data': ''
                   } 
            return result
        else:
            data = parse(content)
            result = {
                    'code': 0,
                    'message': '',
                   } 
            result['data'] = data
            return result


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
            a['entity_flag'] = symptom_flag
            segment_result.append(a)
            id += 1
        
        segment_result = [item for item in segment_result if item['word'] not in ['<', '>', '']]
        result = {
                    'code': 0,
                    'message': '',
                   } 
        result['data'] = segment_result
        return result


class sentiment(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('content', type=str)
        content = parser.parse_args()['content']
        result = predict_model(content)

        result_list = []
        single_dic = {}
        for i, j in result.items():
            single_dic.update(j)
        for word, value in single_dic.items():
            result_dic = {}
            result_dic['word'] = word
            result_dic['positive'] = value
            result_list.append(result_dic)
        
        result_finally = {
            'code': 0,
            'message': '',
           } 
        result_finally['data'] = result_list
        return result_finally


# type = 8 -- 计算短文本相似度
# type = 9 -- 计算语义相似度
class text_similar(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('content1', type=str)
        parser.add_argument('content2', type=str)
        parser.add_argument('type', type=int)

        content1 = parser.parse_args()['content1']
        content2 = parser.parse_args()['content2']
        type = parser.parse_args()['type']
        
        if type == 8:
            if len(content1) > 50 or len(content2) > 50:
                return jsonify({'message': '短文本相似度分析文本长度超过50'})
        if type == 9:
            if len(content1) > 10 or len(content2) > 10:
                return jsonify({'message': '语义相似度分析文本长度超过10'})
            
        result = cal_similarity(content1, content2, type)
        if result < 0:
            result = np.fabs(result)
        result_json = {}
        result_json['similar_vlaue'] = result
        
        result_finally = {
            'code': 0,
            'message': '',
           } 
        result_finally['data'] = result_json
        return result_finally


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


category_dict = {
        0: '宝宝饮食',
        1: '宝宝尿布',
        2: '学前教育',
        3: '小儿肺炎',
        4: '小儿五官',
        5: '小儿脑瘫',
        6: '宝宝睡眠',
        7: '小儿多动症',
        8: '小儿皮肤',
        9: '小儿感冒',
        10: '新生儿黄疸',
        11: '小儿哮喘',
        12: '胎教',
        13: '手足口病',
        14: '婴幼儿腹泻',}

class classifier(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('content', type=str)
        content = parser.parse_args()['content']

        try:

            # print(result)
            # return jsonify({'state': '0'})
            result = text_classifier(content)
            result_json = {}
            result_json['class_num'] = result
            result_json['class_description'] = category_dict[result]
            
            result_finally = {
            'code': 0,
            'message': '',
           } 
            result_finally['data'] = result_json
            return result_finally
        except:
            result_finally = {
            'code': 1,
            'message': '文本分类失败',
           } 
            result_finally['data'] = ''
            return result_finally


api.add_resource(classifier, '/classifier')
api.add_resource(w2v, '/w2v')
api.add_resource(text_similar, '/text_similar')
api.add_resource(sentiment, '/sentiment')
api.add_resource(parser_ltp, '/parser')
api.add_resource(segmentor,'/segmentor')
api.add_resource(freq, '/freq')
api.add_resource(entity, '/entity')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5555)
#    app.run(host='127.0.0.1', debug=True, port=5555)