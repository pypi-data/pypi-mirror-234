#import pdfTableJson.converter2 as converter2  # package # utf-8
import converter
import converter2
import json

# PDF 파일 경로
# merge 작업
# path = "C:/Users/aria1/OneDrive/바탕 화면/프로젝트/pdf_아리사/자료/list/a.pdf" # 세로나뉨
#path = "C:/Users/aria1/OneDrive\바탕 화면\프로젝트\pdf_아리사\추가 샘플자료\오류 PDF.pdf" # 가로나뉨 두번째 부터
#path = "C:/Users/aria1/OneDrive/바탕 화면/프로젝트/pdf_아리사/자료/list/c.pdf" # 가로나뉨 마지막만


# 추가 자료
# path = "C:/Users/aria1/OneDrive\바탕 화면\프로젝트\pdf_아리사\추가 샘플자료/가등기.pdf"
# path = "C:/Users/aria1/OneDrive\바탕 화면\프로젝트\pdf_아리사\추가 샘플자료\오류 PDF.pdf"
# path = "C:/Users/aria1/OneDrive\바탕 화면\프로젝트\pdf_아리사\추가 샘플자료\신탁등기.pdf" # 텍스트 파서에서 읽지 못함

path = "C:/Users/aria1/OneDrive/바탕 화면/전체자료/집합건물_등기부등본.pdf"

# 기본
exclude_list = ['열\n', '열 \n', '람\n', '람 \n', '용\n', '용 \n', '열 람\n', '열 람 \n', '람 용\n', '람 용 \n', '열 람 용\n', '열 람 용 \n', '열람\n', '열람 \n', '람용\n', '람용 \n', '열람용\n', '열람용 \n']
# 추가
exclude_list += ['용 ']
result = converter.main(path, exclude_list)

# print("===================================================================")
# result = json.dumps(result, indent=4, ensure_ascii=False)
# print(result)