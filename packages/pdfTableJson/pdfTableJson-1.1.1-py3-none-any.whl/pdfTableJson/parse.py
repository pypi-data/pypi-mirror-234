import pdfTableJson.converter as converter
import json

# PDF 파일 경로
path = "C:/Users/aria1/OneDrive/바탕 화면/프로젝트/pdf처리/자료/등기부등본모음/집합건물_등기부등본.pdf"
result = converter.main(path)

print(result)