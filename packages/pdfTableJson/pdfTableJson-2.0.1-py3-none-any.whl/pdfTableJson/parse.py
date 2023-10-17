import pdfTableJson.converter_normal as converter_normal
import json

# PDF 파일 경로
path = "C:/Users/aria1/OneDrive/바탕 화면/프로젝트/pdf처리/자료/등기부등본모음/집합건물_등기부등본.pdf"
result = converter_normal.main(path)

print(result)