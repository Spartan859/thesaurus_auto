#百度通用翻译API,不包含词典、tts语音合成等资源，如有相关需求请联系translate_api@baidu.com
# coding=utf-8
 
import http.client
import csv
import hashlib
from typing import final
import urllib
import random
import json
from pip._vendor.distlib.compat import raw_input
from get_thesaurus import get_thesaurus

def translate(q):
# 百度appid和密钥需要通过注册百度【翻译开放平台】账号后获得
    appid = '20220727001285087'        # 填写你的appid
    secretKey = '91sCQtHg_hg_90rxGXe_'    # 填写你的密钥
    
    httpClient = None
    myurl = '/api/trans/vip/translate'  # 通用翻译API HTTP地址
    
    fromLang = 'auto'       # 原文语种
    toLang = 'en'           # 译文语种
    salt = random.randint(32768, 65536)
    # 手动录入翻译内容，q存放
    #q = raw_input("please input the word you want to translate:")
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + \
            '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign
    
    # 建立会话，返回结果
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)
        text=result['trans_result'][0]['dst']
    
    except Exception as e:
        print (e)
    finally:
        if httpClient:
            httpClient.close()
    return text

words=[]
final_ans=[]
with open("words.csv",encoding="utf-8") as file:
    csv_reader=csv.reader(file)
    for row in csv_reader:
        final_ans.append(row[0])
        text=row[0].split('\xa0')[1].split('：')[0].split('，')
        print(text)
        words.append(text)
    file.close()

filewt=open("ans.csv","w",encoding="utf-8")

for row in range(0,len(words)):
    dic=words[row]
    ans=dic[0]
    ans=translate(ans)
    print(ans)
    if(len(ans)>15):
        filewt.write(final_ans[row]+','+ans+'\n')
        continue
    ans=get_thesaurus(ans)
    filewt.write(final_ans[row]+','+ans+'\n')
    print(ans)
