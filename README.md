# free-google-translate
Free Google Translator API 免费的Google翻译

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
YLGoogleTranslate *googleTrans = [[YLGoogleTranslate alloc] init];
[googleTrans translateWithText:content targetLanguageCode:_targetLanguage completion:^(NSString * _Nullable originalText, NSString * _Nullable originalLanguageCode, NSString * _Nullable translatedText, NSString * _Nullable targetLanguageCode, NSString * _Nullable error) {
    if ([error length] > 0) {
        NSLog(@"调用Google翻译接口返回错误：%@ ", error); 
    } else {
        NSLog(@"调用Google翻译接口返回成功！");
    }
}];
```
传入一段待翻译的文本，和目标翻译语言code，然后你就会得到翻译结果，该接口会自动识别输入的语言code


