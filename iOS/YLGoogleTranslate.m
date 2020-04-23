//
//  YLGoogleTranslate.m
//  YoouliOS
//
//  Created by VictorZhang on 2020/4/23.
//  Copyright © 2020 victor. All rights reserved.
//

#import "YLGoogleTranslate.h"
#import "NSString+Category.h"


@interface YLGoogleTranslate()

@property (nonatomic, strong) NSString *url;
@property (nonatomic, strong) NSString *TKK;
@property (nonatomic, strong) NSString *token; // 动态的token，从后台返回
@property (nonatomic, strong) NSDictionary *header;
@property (nonatomic, strong) NSMutableDictionary *data;

@end


@implementation YLGoogleTranslate

- (instancetype)init {
    self = [super init];
    if (self) {
        _url = @"https://translate.google.cn/translate_a/single";
        _TKK = @"434674.96463358";  // 随时都有可能需要更新的TKK值
        _header = @{
                        @"accept": @"*/*",
                        @"accept-language": @"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                        @"cookie": @"NID=188=M1p_rBfweeI_Z02d1MOSQ5abYsPfZogDrFjKwIUbmAr584bc9GBZkfDwKQ80cQCQC34zwD4ZYHFMUf4F59aDQLSc79_LcmsAihnW0Rsb1MjlzLNElWihv-8KByeDBblR2V1kjTSC8KnVMe32PNSJBQbvBKvgl4CTfzvaIEgkqss",
                        @"referer": @"https://translate.google.cn/",
                        @"user-agent": @"Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
                        @"x-client-data": @"CJK2yQEIpLbJAQjEtskBCKmdygEIqKPKAQi5pcoBCLGnygEI4qjKAQjxqcoBCJetygEIza3KAQ==",
                    };
        NSDictionary *reqData = @{
                                    @"client": @"webapp",  // 基于网页访问服务器
                                    @"sl": @"auto",  // 源语言,auto表示由谷歌自动识别
                                    @"tl": @"en",  // 翻译的目标语言
                                    @"hl": @"zh-CN",  // 界面语言选中文，毕竟URL是cn后缀
                                    @"dt": @[@"at", @"bd", @"ex", @"ld", @"md", @"qca", @"rw", @"rm", @"ss", @"t"],  // dt表示要求服务器返回的数据类型
                                    @"otf": @"2",
                                    @"ssel": @"0",
                                    @"tsel": @"0",
                                    @"kc": @"1",
                                    @"tk": @"",  // 谷歌服务器会核对的token
                                    @"q": @""  // 待翻译的字符串
                                };
        _data = [NSMutableDictionary dictionaryWithDictionary:reqData];
    }
    return self;
}

- (void)getTKKInCompletion:(void (^)(NSString * _Nullable tkkData, NSString * _Nullable error))completionHandler {
    NSString *url = @"https://translate.google.cn/";
    [self requestWithUrl:url method:@"GET" header:self.header completionHandler:^(NSData * _Nullable respData, NSError * _Nullable error) {
        if (error) {
            completionHandler(nil, error.localizedDescription);
            return;
        }
        NSString *pageSource = [[NSString alloc] initWithData:respData encoding:NSUTF8StringEncoding];
        NSError *regError = NULL;
        NSString *pattern = @"tkk:'([0-9]+\\.[0-9]+)'";
        NSRegularExpression *regex = [NSRegularExpression regularExpressionWithPattern:pattern options:NSRegularExpressionCaseInsensitive error:&regError];
        if (regError) {
            completionHandler(nil, nil);
            return;
        }
        NSRange rangeOfFirstMatch = [regex rangeOfFirstMatchInString:pageSource options:0 range:NSMakeRange(0, [pageSource length])];
        if (!NSEqualRanges(rangeOfFirstMatch, NSMakeRange(NSNotFound, 0))) {
            NSString *substringForFirstMatch = [pageSource substringWithRange:rangeOfFirstMatch];
            completionHandler(substringForFirstMatch, nil);
        } else {
            completionHandler(nil, nil);
        }
    }];
}

- (void)getTokenWithText:(NSString *)text completion:(void (^)(NSString * _Nullable tokenData, NSString * _Nullable error))completionHandler {
    // 获取google翻译接口的token
    NSString *_tkk = [[self.TKK stringByReplacingOccurrencesOfString:@"'" withString:@""] stringByReplacingOccurrencesOfString:@"tkk:" withString:@""];
    NSString *url = [NSString stringWithFormat:@"http://52.81.95.198:8080/api/google/token?text=%@&tkk=%@", [text urlencode], _tkk];
    [self requestWithUrl:url method:@"GET" header:nil completionHandler:^(NSData * _Nullable respData, NSError * _Nullable error) {
        if (error) {
            completionHandler(nil, error.localizedDescription);
            return;
        }
        NSDictionary *respDict = [NSJSONSerialization JSONObjectWithData:respData options:NSJSONReadingAllowFragments error:nil];
        if (respDict[@"token"]) {
            completionHandler(respDict[@"token"], nil);
        } else {
            completionHandler(nil, nil);
        }
    }];
}

- (void)translateWithText:(NSString *)text
       targetLanguageCode:(NSString *)languageCode
               completion:(void (^)(NSString * _Nullable originalText,
                                    NSString * _Nullable originalLanguageCode,
                                    NSString * _Nullable translatedText,
                                    NSString * _Nullable targetLanguageCode,
                                    NSString * _Nullable error))completionHandler{
    dispatch_group_t _dispatchGroup = dispatch_group_create();
    dispatch_queue_t globalQueue = dispatch_get_global_queue(0, 0);
       
    __weak typeof(self) WEAKSELF = self;
    dispatch_group_enter(_dispatchGroup);
    dispatch_group_async(_dispatchGroup, globalQueue, ^{
//        TKK获取太慢了，容易超时
//        [self getTKKInCompletion:^(NSString * _Nullable tkkData, NSString * _Nullable error) {
//            WEAKSELF.TKK = tkkData;
            [WEAKSELF getTokenWithText:text completion:^(NSString * _Nullable tokenData, NSString * _Nullable error) {
                WEAKSELF.token = tokenData;
                dispatch_group_leave(_dispatchGroup);
            }];
//        }];
    });
    
    dispatch_group_notify(_dispatchGroup, globalQueue, ^{
        self.data[@"q"] = [text urlencode];
        self.data[@"tk"] = self.token;
        self.data[@"tl"] = languageCode;
        NSString *apiurl = [self constructUrl];
        [self requestWithUrl:apiurl method:@"GET" header:self.header completionHandler:^(NSData * _Nullable respData, NSError * _Nullable error) {
            if (error) {
                completionHandler(text, nil, nil, nil, error.localizedDescription);
                return;
            }
            NSError *translatedError = nil;
            NSArray *respArr = [NSJSONSerialization JSONObjectWithData:respData options:NSJSONReadingAllowFragments error:&translatedError];
            if (translatedError) {
                completionHandler(text, nil, nil, nil, translatedError.localizedDescription);
                return;
            }
            NSString *translatedText = @"";
            for (NSArray *subarr in [respArr firstObject]) {
                if ([subarr isKindOfClass:[NSArray class]]) {
                    if ([subarr firstObject] == [NSNull null]) {
                        break;
                    }
                    translatedText = [NSString stringWithFormat:@"%@%@", translatedText, [subarr firstObject]];
                }
            }
            if ([translatedText length] <= 0) {
                  translatedText = [[[respArr firstObject] firstObject] firstObject];
            }
            NSString *originLanguageCode = respArr[2];
            dispatch_async(dispatch_get_main_queue(), ^{
                completionHandler(text, originLanguageCode, translatedText, languageCode, nil);
            });
        }];
    });
}

- (NSString *)constructUrl {
    NSString *base = @"";
    for (NSString *key in [self.data allKeys]) {
        if ([self.data[key] isKindOfClass:[NSArray class]]) {
            NSArray *valueArr = self.data[key];
            NSString *dtStr = @"";
            for (NSString *s in valueArr) {
                if ([dtStr length] > 0) {
                    dtStr = [NSString stringWithFormat:@"%@&dt=%@", dtStr, s];
                } else {
                    dtStr = [NSString stringWithFormat:@"%@dt=%@", dtStr, s];
                }
            }
            base = [NSString stringWithFormat:@"%@%@&", base, dtStr];
        } else {
            base = [NSString stringWithFormat:@"%@%@=%@&", base, key, self.data[key]];
        }
    }
    base = [base substringToIndex:[base length] - 1];
    base = [NSString stringWithFormat:@"%@?%@", self.url, base];
    
    return base;
}

- (void)requestWithUrl:(NSString *)apiUrlStr method:(NSString *)method header:(NSDictionary *_Nullable)header completionHandler:(nullable void (^)(NSData * _Nullable respData,  NSError * _Nullable error))completionHandler {
    NSURL *url = [[NSURL alloc] initWithString:apiUrlStr];
    NSMutableURLRequest *request = [[NSMutableURLRequest alloc] initWithURL:url];
    [request setHTTPMethod:method];
    if (header) {
        [request setAllHTTPHeaderFields:header];
    }
    NSURLSessionDataTask *task = [[NSURLSession sharedSession] dataTaskWithRequest:request completionHandler:^(NSData * _Nullable data, NSURLResponse * _Nullable response, NSError * _Nullable error) {
        completionHandler(data, error);
    }];
    [task resume];
}


@end
