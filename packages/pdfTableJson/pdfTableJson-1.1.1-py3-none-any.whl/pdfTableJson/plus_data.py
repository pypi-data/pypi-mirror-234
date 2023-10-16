import fitz
import re

def getAllData(input_path):
    doc = fitz.open(input_path)
    all_text = []
    for page in doc:
        text = page.get_text()
        all_text.append(text)

    return all_text

'''
def getAllData(input_path):
    doc = fitz.open(input_path)
    all_text = []
    # 첫 번째 페이지만 사용
    first_page = doc[0]
    text = first_page.get_text()
    all_text.append(text)

    return all_text
'''

def textParser(all_text):
    info_dict = {}

    for text in all_text:
            
        # 정규 표현식 패턴 정의
        pattern = r"\[집합건물\]\s+(.*?)\n|고유번호\s+(.*?)\n|열람일시\s+:\s+(.*?)\n|관할등기소\s+(.*?)\n"

        # 정규 표현식을 사용하여 정보 추출
        matches = re.findall(pattern, text)

        for match in matches:
            if match[0]:  # [집합건물] 정보를 찾은 경우
                info_dict["집합건물"] = match[0]
            elif match[1]:  # 고유번호를 찾은 경우
                info_dict["고유번호"] = match[1]
            elif match[2]:  # 열람일시를 찾은 경우
                info_dict["열람일시"] = match[2]
            elif match[3]:  # 관할등기소를 찾은 경우
                info_dict["관할등기소"] = match[3]

    return info_dict