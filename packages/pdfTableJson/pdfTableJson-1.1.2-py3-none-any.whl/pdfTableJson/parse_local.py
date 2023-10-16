#import pdfTableJson.converter2 as converter2  # package # utf-8
import converter
import converter2
import json

# PDF 파일 경로
#path = "C:/Users/aria1/OneDrive/바탕 화면/프로젝트/pdf_아리사/자료2/004.pdf"

#path = "C:/Users/aria1/OneDrive/바탕 화면/프로젝트/pdf_아리사/자료/list/a.pdf" # 세로나뉨
#path = "C:/Users/aria1/OneDrive\바탕 화면\프로젝트\pdf_아리사\추가 샘플자료\오류 PDF.pdf" # 가로나뉨 두번째 부터
path = "C:/Users/aria1/OneDrive/바탕 화면/프로젝트/pdf_아리사/자료/list/c.pdf" # 가로나뉨 마지막만


# 기본
exclude_list = ['열\n', '열 \n', '람\n', '람 \n', '용\n', '용 \n', '열 람\n', '열 람 \n', '람 용\n', '람 용 \n', '열 람 용\n', '열 람 용 \n', '열람\n', '열람 \n', '람용\n', '람용 \n', '열람용\n', '열람용 \n']
# 추가
exclude_list += ['용 ']
result = converter2.main(path, exclude_list)

# print("===================================================================")

# print(result)