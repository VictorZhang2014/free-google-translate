# -*- coding:utf-8 -*-
# 网友的建议：https://github.com/VictorZhang2014/free-google-translate/issues/6
# 

import urllib.parse
import requests
import json
import re
import ssl
import ctypes
import time

ssl._create_default_https_context = ssl._create_unverified_context


class GoogleTrans(object):
    def __init__(self):
        self.url = 'https://translate.google.cn/translate_a/single'
        self.TKK = "434674.96463358"  # 随时都有可能需要更新的TKK值
        
        self.header = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9",
            "cookie": "NID=188=M1p_rBfweeI_Z02d1MOSQ5abYsPfZogDrFjKwIUbmAr584bc9GBZkfDwKQ80cQCQC34zwD4ZYHFMUf4F59aDQLSc79_LcmsAihnW0Rsb1MjlzLNElWihv-8KByeDBblR2V1kjTSC8KnVMe32PNSJBQbvBKvgl4CTfzvaIEgkqss",
            "referer": "https://translate.google.cn/",
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

    class JSHackToken():
        def rshift(self, val, n): return (val % 0x100000000) >> n
        def Number(self, val):
            try:
                return eval(val, {}, {})
            except:
                return 0
        class Undefined:
            def __init__():
                pass
        class js_array():
            def __init__(self, outer, init=[]):
                self.outer = outer
                self.storage = list(init).copy()
            def __getitem__(self, key):
                if (type(key).__name__ != 'int'):
                    if (type(key).__name__ == 'float') and int(key) != key:
                        return 0
                    try:
                        key = int(key)
                    except:
                        return 0
                if len(self.storage)<=key or key<0:
                    return 0
                return self.storage[key]
            def __setitem__(self, key, value):
                if (type(key).__name__ != 'int'):
                    if (type(key).__name__ == 'float') and int(key) != key:
                        return 0
                    try:
                        key = int(key)
                    except:
                        return 0
                if key<0:
                    return 0
                while key >= len(self.storage):
                    self.storage.append(0)
                self.storage[key] = value
                return
            def __len__(self):
                return len(self.storage)
            def __str__(self):
                return self.storage.__str__()
            def __repr__(self):
                return self.storage.__repr__()
        def array(self, init = []):
            return self.js_array(self, init)
        def uo(self, a, b):
            for c in range(0, len(b)-2, 3):
                d = b[c+2]
                if 'a' <= d:
                    d = ord(d)-87
                else:
                    d = self.Number(d)
                if '+' == b[c+1]:
                    d = self.rshift(a, d)
                else:
                    d = a<<d
                if b[c] == "+":
                    a = a + d & 4294967295
                else:
                    a = a ^ d
            return a
        def wo(self, a, tkk):
            d = self.array(init = tkk.split("."))
            b = self.Number(d[0])
            e = self.array()
            f = 0
            g = 0
            while g < len(a):
                h = ord(a[g])
                if 128 > h:
                    e[f] = h
                    f += 1
                else:
                    if 2048 > h:
                        e[f] = h >> 6 | 192
                        f += 1
                    else:
                        if (55296 == (h & 64512)) and (g + 1 < len(a)) and (56320 == (ord(a[g+1]) & 64512)):
                            h = 65536 + ((h & 1023) << 10) + (ord(a[g+1]) & 1023)
                            g += 1
                            e[f] = h >> 18 | 240
                            f += 1
                            e[f] = h >> 12 & 63 | 128
                            f += 1
                        else:
                            e[f] = h >> 12 | 224
                            f += 1
                            e[f] = h >> 6 & 63 | 128
                            f += 1
                    e[f] = h & 63 | 128
                    f += 1
                g += 1
            a = b
            
            for f in range(0, len(e)):
                a += e[f]
                a = ctypes.c_long(a).value
                a = self.uo(a, '+-a^+6')
            a = self.uo(a, '+-3^+b+-f')
            a ^= self.Number(d[1])
            if 0 > a:
                a = (a & 2147483647)+2147483648
            a %= 10**6
            return str(a)+'.'+str(a^b)
        
        # 构建完对象以后要同步更新一下TKK值
        # self.update_TKK()  
    
    
    def update_TKK(self):
        url = "https://translate.google.cn/"
        req = requests.get(url, headers=self.header)
        page_source = req.text
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
        q = re.sub('''[^\u2E80-\u9FFF \n\t\w_.!'"`+-=——,$%^，。？、~@#￥%……|[\]&\\*《》<>「」{}【】()/]''', '', q)
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
    print("==============================")
    print(originalText, originalLanguageCode, targetText, targetLanguageCode)
