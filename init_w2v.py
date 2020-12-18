# -*- encoding:utf-8 -*-
'''
    input: 一段需要分词的文本
    output: 结果更新于文件夹 temp/result_symptomDic.json --- 症状对应的位置【json格式】
'''
import re
import subprocess
import sys


def read_lines(path):
    all_lines = []
    with open(path, 'r', encoding='utf-8') as file:
        temp_lines = file.readlines()
        for line in temp_lines:
            line = line.strip()
            if line:
                all_lines.append(line)
    return all_lines


def set_dta(keywords):
    p = []
    for word in keywords:
        ln = len(word)
        char = word[ln-1]
        if not (char in p):
            p.append(char)
    p = set(p)
    return p


pattern_sub = re.compile(' ')


def Dictest(line, view_dict_set,keywords):
    
    # 字典特征提取（采用倒序搜索算法）
    newline_flag = ('。', '！', '？')
    if line[-1] not in newline_flag:
        line = line + '。'
    line = pattern_sub.sub('_',line)  # '_'替换空格等
    
    aresult = '/temp/test_Dic'
    fa = open(sys.path[0] + aresult,'w',encoding='utf-8')
    word = []
    dic = []
    for w in line:
        word.append(w)
        dic.append('O') 
    ln = len(word)
    i = ln
    j = 0
    le = []
    while i-j > 0:
        t = ''.join(word[i-1:i])
        if not (t in view_dict_set):
            j = 0
            i -= 1
            continue
        for k in range(1,min(10,ln+1)):
            if ''.join(word[i-k:i]) in keywords:
                le.append(k)
        if len(le) == 0:
            i = i-1
        if len(le) > 0:
            if len(le) == 1:
                if le[0] == 1:
                    dic[i-1] = 'S-CAR'
                    continue
                else:
                    dic[i-le[0]] = 'B-CAR'
                    for h in range(i-le[0]+1, i-1, 1):
                        dic[h] = 'I-CAR'
                    dic[i-1] = 'E-CAR'
                    i = i-le[0]
                    le = []
                    continue
            if len(le) == 2:
                if le[1] == 1:
                    dic[i-1] = 'S-CAR'
                    continue
                else:
                    dic[i-le[1]] = 'B-CAR'
                    for h in range(i-le[1]+1, i-1, 1):
                        dic[h] = 'I-CAR'
                    dic[i-1] = 'E-CAR'
                    i = i-le[1]
                    le = []
                    continue
            if len(le) > 2:
                if le[2] == 1:
                    dic[i-1] = 'S-CAR'
                    continue
                else:
                    dic[i-le[2]] = 'B-CAR'
                    for h in range(i-le[2]+1, i-1, 1):
                        dic[h] = 'I-CAR'
                    dic[i-1] = 'E-CAR'
                    i = i-le[2]
                    le = []
                    continue
    for m in range(len(word)):
        fa.write(word[m]+'\t'+dic[m]+'\n')
    fa.write('\n')
    word = []
    dic = []


def crf_prodict():
    # win
    crf_test_exe = r'.\crf_tool\crf_test '
    model = r' -m .\model\Dic_model'
    # 进行测试
    test = r' .\temp\test_Dic'
    output = r' .\temp\test_Dic_Result'
    process = subprocess.Popen(crf_test_exe + model +test + ' >' + output, shell=True)
    process.wait()  # 堵塞式


def toJson():
    fout = open('temp/result_symptomDic.json', 'w', encoding='utf-8')
    index = 0
    fout.write('[')
    
    fin = open('temp/test_Dic_Result', 'r', encoding='utf-8')
    Tlist = []
    view = []
    lines = fin.readlines()
    for line in lines:
        if line.strip():
            tag = line.strip().split()[2]
            Tlist.append(tag)
    SE = []
    for i in range(len(Tlist)):
        if Tlist[i] == 'S-CAR':
            SE.append(i)
            SE.append(i)
            view.append(SE)
            # index += 1
            SE = []
        if Tlist[i] == 'B-CAR':
            SE.append(i)
        if Tlist[i] == 'E-CAR':
            SE.append(i)
            view.append(SE)
            SE = []
    index += len(view)
    fout.write('{"View":%s' % str(view)+'}')
    fout.write(']')
    fout.close()


def init(text):
    
    fVar = open('dict/symptom.txt', 'r', encoding='utf-8')
    keywords = []
    ViewLines = fVar.readlines()
    for line in ViewLines:
        if line.strip():
            word = line.strip()
            keywords.append(word)

    view_dict_set = set_dta(keywords)
    Dictest(text, view_dict_set, keywords)
    crf_prodict()  # CRF++预测结果更新
    toJson()
