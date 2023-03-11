#! /usr/bin/env python
# -*- coding:utf-8 -*-

import urllib.request
import urllib.parse
import json
import execjs
import re
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class GoogleTrans(object):
    def __init__(self):
        self.url = 'https://translate.google.com.hk/translate_a/single'
        self.TKK = "434674.96463358"  # 随时都有可能需要更新的TKK值
        
        self.header = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9",
            "cookie": "NID=188=M1p_rBfweeI_Z02d1MOSQ5abYsPfZogDrFjKwIUbmAr584bc9GBZkfDwKQ80cQCQC34zwD4ZYHFMUf4F59aDQLSc79_LcmsAihnW0Rsb1MjlzLNElWihv-8KByeDBblR2V1kjTSC8KnVMe32PNSJBQbvBKvgl4CTfzvaIEgkqss",
            "referer": "https://translate.google.com.hk/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
            "x-client-data": "CJK2yQEIpLbJAQjEtskBCKmdygEIqKPKAQi5pcoBCLGnygEI4qjKAQjxqcoBCJetygEIza3KAQ==",
        }
        
        self.data = {
            "client": "webapp",  # 基于网页访问服务器
            "sl": "auto",  # 源语言,auto表示由谷歌自动识别
            "tl": "vi",  # 翻译的目标语言
            "hl": "zh-CN",  # 界面语言选中文，毕竟URL都是cn后缀了，就不装美国人了
            "dt": ["at", "bd", "ex", "ld", "md", "qca", "rw", "rm", "ss", "t"],  # dt表示要求服务器返回的数据类型
            "otf": "2", 
            "ssel": "0",
            "tsel": "0",
            "kc": "1",
            "tk": "",  # 谷歌服务器会核对的token
            "q": ""  # 待翻译的字符串
        }
        
        with open('token.js', 'r', encoding='utf-8') as f:  
            self.js_fun = execjs.compile(f.read())

        # 构建完对象以后要同步更新一下TKK值
        # self.update_TKK()  
    
    
    def update_TKK(self):
        url = "https://translate.google.com.hk/"
        req = urllib.request.Request(url=url, headers = self.header)
        page_source = urllib.request.urlopen(req).read().decode("utf-8")
        self.TKK = re.findall(r"tkk:'([0-9]+\.[0-9]+)'", page_source)[0]
        
        
    def construct_url(self):
        base = self.url + '?'
        for key in self.data:
            if isinstance(self.data[key], list):
                base = base + "dt=" + "&dt=".join(self.data[key]) + "&"
            else:
                base = base + key + '=' + self.data[key] + '&'
        base = base[:-1]
        return base
    
    def query(self, q, lang_to=''):
        q = re.sub('''[^\u2E80-\u9FFF \n\t\w_.!'"“”`+-=——,$%^，。？、~@#￥%……|[\]&\\*《》<>「」{}【】()/]''', '', q)
        retry = 3
        while retry > 0:
            try:
                self.data['q'] = urllib.parse.quote(q)
                self.data['tk'] = self.JSHackToken().wo(q, self.TKK)
                self.data['tl'] = lang_to
                url = self.construct_url()
                robj = requests.post(url)
                response = json.loads(robj.text)
                targetText = ''
                for item in response[0]:
                    if item[0]:
                        targetText += item[0]
                originalText = response[0][0][1]
                originalLanguageCode = response[2]
                print("翻译前：{}，翻译前code：{}".format(originalText, originalLanguageCode))
                print("==============================")
                print("翻译后：{}, 翻译后code：{}".format(targetText, lang_to))
                return originalText, originalLanguageCode, targetText, lang_to
            except Exception as e:
                print(e)
                retry -= 1
                time.sleep(2)


if __name__ == '__main__':
    text = "Hello world"
    originalText, originalLanguageCode, targetText, targetLanguageCode = GoogleTrans().query(text, lang_to='zh-CN')  
    print(originalText, originalLanguageCode, targetText, targetLanguageCode)
    


