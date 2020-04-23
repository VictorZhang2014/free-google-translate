//
//  YLGoogleTranslate.h
//  YoouliOS
//
//  Created by VictorZhang on 2020/4/23.
//  Copyright © 2020 victor. All rights reserved.
//

#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

@interface YLGoogleTranslate : NSObject

- (void)translateWithText:(NSString *)text
       targetLanguageCode:(NSString *)languageCode
               completion:(void (^)(NSString * _Nullable originalText,
                                    NSString * _Nullable originalLanguageCode,
                                    NSString * _Nullable translatedText,
                                    NSString * _Nullable targetLanguageCode,
                                    NSString * _Nullable error))completionHandler;

@end

NS_ASSUME_NONNULL_END
