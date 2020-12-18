#! python3
# coding: utf-8

from pyltp import Parser
from cut_seg_tag_parser import build_test_data_from_crf
from flask import jsonify


def segmentor_tag(content):
    result = build_test_data_from_crf(content)
#    [{'term': '你', 'type': 'r'}, 
#     {'term': '过', 'type': 'ug'}, 
#     {'term': '单词', 'type': 'symptom'}, 
#     {'term': '扩', 'type': 'v'}, 
#     {'term': '展包', 'type': 'symptom'}, 
#     {'term': '>', 'type': 'x'}, 
#     {'term': '', 'type': 'symptom'},
#     {'term': '<', 'type': 'x'}]
    
# 2018_1_6: find that the formula of the result is abnormal(as above)
# result will always end with ['', '<', '>']
#    for i in result:
#        if i['term'] in ['', '<', '>'] or len(i['term']) == 0:
#            result.remove(i)
#    result.pop()
#    print (result)  
    result = [item for item in result if item['term'] not in ['<', '>', '']]      
    words_list = []
    tags_list = []
    symptom_flag_list = []
    for item in result:
        words_list.append(item['term'])
        if item['type'] == 'symptom':
            symptom_flag_list.append(1)
            item['type'] = 'symptom'
        else:
            symptom_flag_list.append(0)
        tags_list.append(item['type'])
    return words_list,tags_list,symptom_flag_list


def parse(content):
    words_list, tags_list, symptom_flag_list = segmentor_tag(content)
    print(words_list, tags_list, symptom_flag_list)
    parser = Parser()  # 初始化实例
    try:
        parser.load('./ltp/ltp_data/parser.model')  # 加载模型
    except:
        print('load parser model failed, can not find model in ./ltp/ltp_data/parser.model')
#        parser.load('C:\\Users\\01055221\\Desktop\\API_NLP\\ltp\\ltp_data\\parser.model')  # 加载模型
    # 模型地址重新部署时需要更新
#    test = parser.parse(['患者', '无', '胸痛'],
#                        ['n', 'v', 'n'])
#    for i in test:
#        print (i.head)
#        print ('-------')
    arcs = parser.parse(words_list,tags_list)  # 句法分析
    parser.release()  # 释放模型
    if len(content) > 0:
        b = []
        i = 0
        for arc in arcs:
            i += 1
            c = {}
            c['ID'] = i
            c['LEMMA'] = words_list[i-1]
            c['POSTAG'] = tags_list[i-1]
            c['SYMPTOM_FLAG'] = symptom_flag_list[i-1]
            c['HEAD'] = arc.head
            c['RELATION'] = arc.relation
            b.append(c)
        return b
    else:
        return jsonify({'message': {'content': '长度不得为零'}})