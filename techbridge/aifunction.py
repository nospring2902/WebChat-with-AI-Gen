import google.generativeai as genai
from datetime import datetime
import os
from .local_settings import API_KEY

# Cấu hình API với khóa API của bạn
genai.configure(api_key=API_KEY)

# Tạo một đối tượng model từ Gemini
model = genai.GenerativeModel('gemini-1.5-flash')

def summarize_text(paragraph):
    PROMPT = f"""
    Please make a summary of multiple people's conversation below.
    The longest it can be is 5 sentences. 
    Make sure to include important infromations about developing an app.
    "{paragraph}"
    
    Tóm tắt:
    """
    
    # Gọi API để tóm tắt văn bản
    response = model.generate_content(PROMPT)
    
    # Trả về kết quả tóm tắt
    return response.text.strip()

# Ví dụ sử dụng hàm với đoạn văn bản
paragraph = """
i'm free now can u open ur vs code 
Oh hiiii I'm actually rewriting the code 
So I don't want someone to merge it I'll push the new code later and I want you to check that and merge 
Thank you 
okayyyyy thankyou boss 
I'm free on tomorrow morning so I will try to fix some problems we still have 
Thank youuuuuu 
"""
summary = summarize_text(paragraph)

# In ra tóm tắt
print(summary)