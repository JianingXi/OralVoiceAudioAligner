import os
import re
from PyPDF2 import PdfReader

# 关键词设定（正则匹配换行干扰）
KEYWORDS = [
    re.compile(r"Tertiary\s+Education\s+Scientific\s+research\s+project\s+of\s+Guangzhou\s+Municipal\s+Education\s+Bureau", re.IGNORECASE),
    re.compile(r"202235388")
]

def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        full_text = ''
        for page in reader.pages:
            full_text += page.extract_text() or ''
        return full_text
    except Exception as e:
        print(f"[ERROR] 无法读取PDF：{pdf_path}，错误：{e}")
        return ''

def search_keywords_in_text(text):
    normalized_text = re.sub(r'\s+', ' ', text)  # 将所有空白字符合并成空格
    for pattern in KEYWORDS:
        if pattern.search(normalized_text):
            return True
    return False

def scan_pdfs(root_dir):
    matched_files = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                print(f"[INFO] 正在扫描：{pdf_path}")
                text = extract_text_from_pdf(pdf_path)
                if search_keywords_in_text(text):
                    print(f"[FOUND] 匹配关键词：{pdf_path}")
                    matched_files.append(pdf_path)
    return matched_files

if __name__ == "__main__":
    folder = r"C:\Users\Administrator\Desktop\新建文件夹"  # 修改为你的路径
    results = scan_pdfs(folder)
    print("\n✅ 匹配到以下PDF文件：")
    for path in results:
        print(path)
