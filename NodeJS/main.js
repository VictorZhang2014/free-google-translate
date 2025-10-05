
const { OpenAI } = require("openai");

class TranslatorTS { 
  
    constructor() { 
        // Get your token from here FOR FREE https://huggingface.co/settings/tokens
        this.HF_TOKEN = "YOUR_HUGGINGFACE_TOKEN"; 
    }

    async translate(text, sourceLang, targetLang) {
      if (this.HF_TOKEN == "YOUR_HUGGINGFACE_TOKEN") {
          throw new Error("Please set your Hugging Face API token in the HF_TOKEN variable. Get it from https://huggingface.co/settings/tokens.");
      } 
      const user_message = `Translate '${text}' from ${sourceLang} to ${targetLang}`;
      const messages = [
          {
              "role": "system",
              "content": "You are a powerful translator that can translate any language to any language. You always answer in JSON format with the following keys: originalText, originalLanguageCode, targetText, targetLanguageCode. You never change the keys."
          },
          {
              "role": "user",
              "content": user_message
          }
      ]; 
      const client = new OpenAI({
        baseURL: "https://router.huggingface.co/v1",
        apiKey: this.HF_TOKEN,
      }); 
      const chatCompletion = await client.chat.completions.create({
        model: "deepseek-ai/DeepSeek-V3.2-Exp:novita",
        messages: messages
      });
      return chatCompletion.choices[0].message;
    } 

}

// Example usage:
const translator = new TranslatorTS();
translator.translate("Hello world! I love programming", "English", "Chinese")
.then(response => {
    console.log(response);
});
// Output
// {
//   "originalText": "Hello world! I love programming",
//   "originalLanguageCode": "English",
//   "targetText": "你好，世界！我热爱编程",
//   "targetLanguageCode": "Chinese"
// }