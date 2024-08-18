import google.generativeai as genai
from datetime import datetime
import os
from .local_settings import API_KEY

# Cấu hình API với khóa API của bạn
genai.configure(api_key=API_KEY)

# Tạo một đối tượng model từ Gemini
model = genai.GenerativeModel('gemini-1.5-flash')

def translate(paragraph, language): 
    PROMPT = f"""
    Please translate the following sentence below. Consider yourself is a male. You should provide only 1 version of translation.
    
    Notice that just translate it into 1 version only, for example: don't add Romaji version together with the translated version.
    Don't explain anything more, just translate.

    Now, Translate this into "{language}":
    "{paragraph}"

    """
    
    # Gọi API để tóm tắt văn bản
    response = model.generate_content(PROMPT)
    
    # Trả về kết quả tóm tắt
    return response.text.strip()

def summarize_text(paragraph, language):
    PROMPT = f"""
    Please make a summary of multiple people's conversation below in {language} language.
    The longest it can be is 5 sentences. 
    Make sure to include important informations about developing an app.
    Remember to provide the answer in {language}.
    
    This is the conversation: "{paragraph}"
    """
    # Gọi API để tóm tắt văn bản
    response = model.generate_content(PROMPT)
    
    # Trả về kết quả tóm tắt
    return response.text.strip()

def word_explanation(paragraph,language):
    PROMPT = f"""
    - Detect IT professional vocabulary from the following sentence
    - list out the explanations of the each IT professional vocabularies in 1 sentence.
    - Don't answer anything else than explanation of the words.
    - Let each explanation in one line.
    - Write the reply in {language} language.
    - If there are no IT words detected, answer "No IT words detected"
    "{paragraph}"
    """
    # Gọi API để tóm tắt văn bản
    response = model.generate_content(PROMPT)
    print(response.text.strip())
    # Trả về kết quả tóm tắt
    return response.text.strip()