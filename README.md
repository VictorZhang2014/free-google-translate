# Free Google Translator

[![Generic badge](https://img.shields.io/badge/mit.svg)](https://shields.io/)

Free Google Translate is a tool for google free translation API, the main idea of the repo is coming from the web `https://translate.google.cn` translation, we use a hacking way to access the web translation api for translating text.


# The Do's and Don'ts
- 1.You will get `429 Too many requests` error if you request so many times simultaneously
  - Suggested Solution: To avoid requests in just one IP address, you can put the requesting code in every client (app on device), then it will bypass the IP restriction
- 2.The api service is unavailable if you send large amount of requests at the same time.


# For Python Example
```python
text = "Hello world"
GoogleTrans().query(text, lang_to='zh-CN') 
```
You pass a string of plain text with target language code, then you will get the translated text after requested. the request api will recognize the source language of the text automatically for you.

The output will be:
```
Before translating: "Hello world" with target lange code en
After translating: "你好，世界"
```

<br/>
<br/>

# For Objective-C Example on iOS 
```objective-c
NSString *content = @"Hello world";
NSString *targetLanguage = @"zh-CN";
YLGoogleTranslate *googleTrans = [[YLGoogleTranslate alloc] init];
[googleTrans translateWithText:content targetLanguageCode:targetLanguage completion:^(NSString * _Nullable originalText, NSString * _Nullable originalLanguageCode, NSString * _Nullable translatedText, NSString * _Nullable targetLanguageCode, NSString * _Nullable error) {
    if ([error length] > 0) {
        NSLog(@"The Request returned error! Error Message: %@", error); 
    } else {
        NSLog(@"The Request returned success!!!!!!");
    }
}];
```
The response data is as same as aforementioned python code.




<br/>
<br/>
<br/>
<br/>
<br/>
<br/>




# free-google-translate
Free Google Translator API 免费的Google翻译，其中的破解思路主要来源于将 https://translate.google.cn 的web访问方式模拟成全部代码的形式来控制api的访问

# 注意事项
- 1.大量的相同IP请求会导致Google翻译接口返回 429 Too many requests 
   -  建议处理方案：每一个app客户端自己去请求此接口，就可以避免只有一个IP的服务器去请求
- 2.大量的请求也会使此接口的服务不可用


# Python使用
```python
text = "Hello world"
GoogleTrans().query(text, lang_to='zh-CN') 
```
传入一段待翻译的文本，和目标翻译语言code，然后你就会得到翻译结果，该接口会自动识别输入的语言code

输出结果是：
```
翻译前：Hello world，翻译前code：en
翻译后：你好，世界, 翻译后code：zh-CN
```

<br/>
<br/>

# iOS Objective-C使用
```objective-c
NSString *content = @"Hello world";
NSString *targetLanguage = @"zh-CN";
YLGoogleTranslate *googleTrans = [[YLGoogleTranslate alloc] init];
[googleTrans translateWithText:content targetLanguageCode:targetLanguage completion:^(NSString * _Nullable originalText, NSString * _Nullable originalLanguageCode, NSString * _Nullable translatedText, NSString * _Nullable targetLanguageCode, NSString * _Nullable error) {
    if ([error length] > 0) {
        NSLog(@"调用Google翻译接口返回错误：%@ ", error); 
    } else {
        NSLog(@"调用Google翻译接口返回成功！");
    }
}];
```
传入一段待翻译的文本，和目标翻译语言code，然后你就会得到翻译结果，该接口会自动识别输入的语言code


