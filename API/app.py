import google.generativeai as genai
from datetime import datetime
import os
from local_settings import API_KEY

# Cấu hình API với khóa API của bạn
genai.configure(api_key=API_KEY)

# Tạo một đối tượng model từ Gemini
model = genai.GenerativeModel('gemini-1.5-flash')

def summarize_text(paragraph):
    PROMPT = f"""
    Bạn là một AI có khả năng tóm tắt văn bản. 
    Hãy tóm tắt đoạn văn sau thành một đoạn ngắn gọn nhưng đầy đủ ý chính.
    Hãy trả lời bằng Tiếng Anh.
    Đoạn văn: 
    "{paragraph}"
    
    Tóm tắt:
    """
    
    # Gọi API để tóm tắt văn bản
    response = model.generate_content(PROMPT)
    
    # Trả về kết quả tóm tắt
    return response.text.strip()

# Ví dụ sử dụng hàm với đoạn văn bản
paragraph = """
Artificial Intelligence (AI) has revolutionized various industries, including healthcare, finance, and transportation. 
By leveraging machine learning algorithms and vast amounts of data, AI systems can make accurate predictions, 
optimize processes, and even perform tasks that were previously thought to require human intelligence. 
As AI continues to evolve, its impact on society will likely grow, bringing both opportunities and challenges. 
From autonomous vehicles to personalized medicine, the possibilities are endless, 
but so are the ethical considerations and potential risks that come with this powerful technology.
"""
summary = summarize_text(paragraph)

# In ra tóm tắt
print(summary)