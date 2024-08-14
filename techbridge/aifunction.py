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
    Translate this into "{language}":
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
    "{paragraph}"
    """
    
    # Gọi API để tóm tắt văn bản
    response = model.generate_content(PROMPT)
    
    # Trả về kết quả tóm tắt
    return response.text.strip()