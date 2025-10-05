# Added by github.com/VictorZhang2014
# Date: 2025-10-05 21:35

import os
from openai import OpenAI


class TranslatorByDeepSeek:
    
    def __init__(self):
      # Get your token from here FOR FREE https://huggingface.co/settings/tokens
      self.HF_TOKEN = "YOUR_HUGGINGFACE_TOKEN"
    
    def translate(self, text, source_language="en", target_language="fr"):
        if self.HF_TOKEN == "YOUR_HUGGINGFACE_TOKEN":
            raise ValueError("Please set your Hugging Face API token in the HF_TOKEN variable. Get it from https://huggingface.co/settings/tokens.")
        client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=self.HF_TOKEN,
        )
        user_message = f"Translate '{text}' from {source_language} to {target_language}"
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3.2-Exp:novita",
            messages=[
                {
                    "role": "system",
                    "content": "You are a powerful translator that can translate any language to any language. You always answer in JSON format with the following keys: originalText, originalLanguageCode, targetText, targetLanguageCode. You never change the keys."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
        )
        return completion.choices[0].message.content
    



if __name__ == "__main__":
    text = "Hello world! I love China very much."
    translator = TranslatorByDeepSeek()

    # From English to Chinese
    response = translator.translate(text, source_language="en", target_language="zh")
    print(response)

    # Output like this:
    # {
    #   "originalText": "Hello world! I love China very much.",
    #   "originalLanguageCode": "en",
    #   "targetText": "你好，世界！我非常热爱中国。",
    #   "targetLanguageCode": "zh"
    # }
