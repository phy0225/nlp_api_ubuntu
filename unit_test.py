import requests

#http://127.0.0.1:5555/segmentor?content=我写代码突然肚子痛，头晕，好像怀孕了，不知道会不会死
#http://127.0.0.1:5555/entity?content=患者高血压和心脏病五年，现出现反复活动后胸闷、气促、肢肿十余年。偶尔伴有腹胀，出血，质稀，发热，我觉得我有糖尿病
#http://127.0.0.1:5555/freq?content=我写代码突然肚子痛，头晕，好像怀孕了，不知道会不会死。
#http://127.0.0.1:5555/w2v?content=患者十年头疼
#http://127.0.0.1:5555/sentiment?content=患者无明显诱因下出现胸痛，双下肢未见水肿。今补充诊断：肺部感染。患者舌红，苔黄腻，脉弦细予荆银合剂2瓶疏风清热
#http://127.0.0.1:5555/parser?content=患者无明显诱因下出现胸痛，双下肢未见水肿。
#http://127.0.0.1:5555/text_similar?content1=减轻，咳嗽，咳痰，量少色白，质稀，发热&content2=反复活动后胸闷、气促、肢肿十余年。偶尔伴有腹胀，出血，质稀，发热&type=8
#http://127.0.0.1:5555/text_similar?content1=发热&content2=头疼&type=9

unit_pass_count = 0
url_segmentor = 'http://127.0.0.1:5555/segmentor' 
params_segmentor = {'content': '我写代码突然肚子痛，头晕，好像怀孕了'}
test_segmentor = requests.post(url_segmentor, params=params_segmentor)  
print (test_segmentor.json()) 
if test_segmentor.status_code == 200:
    print (test_segmentor.url, '\n------passed------\n')
    unit_pass_count += 1
else:
    print (test_segmentor.url, '\n------failed------\n')
    

url_entity = 'http://127.0.0.1:5555/entity' 
params_entity = {'content': '患者高血压和心脏病五年，现出现反复活动后胸闷、气促、肢肿十余年。偶尔伴有腹胀，出血，质稀，发热，我觉得我有糖尿病'}
test_entity = requests.post(url_entity, params=params_entity)   
print (test_entity.json()) 
if test_entity.status_code == 200:
    print (test_entity.url, '\n------passed------\n')
    unit_pass_count += 1
else:
    print (test_entity.url, '\n------failed------\n')
    

url_freq = 'http://127.0.0.1:5555/freq' 
params_freq = {'content': '我写代码突然肚子痛，头晕，好像怀孕了'}
test_freq = requests.post(url_freq, params=params_freq) 
print (test_freq.json()) 
if test_freq.status_code == 200:
    print (test_freq.url, '\n------passed------\n')
    unit_pass_count += 1
else:
    print (test_freq.url, '\n------failed------\n')


url_w2v = 'http://127.0.0.1:5555/w2v' 
params_w2v = {'content': '患者十年头疼'}
test_w2v = requests.post(url_w2v, params=params_w2v) 
print (test_w2v.json())
if test_w2v.status_code == 200:
    print (test_w2v.url, '\n------passed------\n')
    unit_pass_count += 1
else:
    print (test_w2v.url, '\n------failed------\n')
    

url_sentiment = 'http://127.0.0.1:5555/sentiment' 
params_sentiment = {'content': '患者无明显诱因下出现胸痛，双下肢未见水肿。今补充诊断：肺部感染。患者舌红，苔黄腻，脉弦细予荆银合剂2瓶疏风清热'}
test_sentiment = requests.post(url_sentiment, params=params_sentiment) 
print (test_sentiment.json())
if test_sentiment.status_code == 200:
    print (test_sentiment.url, '\n------passed------\n')
    unit_pass_count += 1
else:
    print (test_sentiment.url, '\n------failed------\n')
    

url_parser = 'http://127.0.0.1:5555/parser' 
params_parser = {'content': '患者无明显诱因下出现胸痛'}
test_parser = requests.post(url_parser, params=params_parser) 
print (test_parser.json())
if test_parser.status_code == 200:
    print (test_parser.url, '\n------passed------\n')
    unit_pass_count += 1
else:
    print (test_parser.url, '\n------failed------\n')


url_text_similar_8 = 'http://127.0.0.1:5555/text_similar' 
params_text_similar_8 = {'content1': '减轻，咳嗽，咳痰，量少色白，质稀，发热',
                       'content2': '反复活动后胸闷、气促、质稀，发热',
                       'type': 8}
test_text_similar_8 = requests.post(url_text_similar_8, params=params_text_similar_8)
print (test_text_similar_8.json())
if test_text_similar_8.status_code == 200:
    print (test_text_similar_8.url, '\n------passed------\n')
    unit_pass_count += 1
else:
    print (test_text_similar_8.url, '\n------failed------\n')

                               
url_text_similar_9 = 'http://127.0.0.1:5555/text_similar' 
params_text_similar_9 = {'content1': '发热',
                       'content2': '头疼',
                       'type': 9}
test_text_similar_9 = requests.post(url_text_similar_9, params=params_text_similar_9) 
print (test_text_similar_9.json())
if test_text_similar_9.status_code == 200:
    print (test_text_similar_9.url, '\n------passed------\n')
    unit_pass_count += 1
else:
    print (test_text_similar_9.url, '\n------failed------\n') 


if __name__ == '__main__':
    print ('total_unit: 8')
    print ('counts of passed units: %s' %unit_pass_count)
                               