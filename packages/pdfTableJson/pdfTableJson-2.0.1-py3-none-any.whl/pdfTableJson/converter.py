import os
import shutil
import cv2
import numpy as np
import json
import argparse
import re # 정규식
import fitz  # PyMuPDF # text extractor

try:
    import util  # package # utf-8 # local
    import group_parser  # package # parser # local
    import plus_data  # package # 추가데이터 # local
    import merge # package # parser # local
except ImportError:
    from . import util  # package # utf-8 # pypi
    from . import group_parser # package # parser # pypi
    from . import plus_data # package # parser # pypi
    from . import merge # package # parser # pypi


# 워터마크 제거
def f_remove_watermark(image, target_color):
    diff = np.abs(image - target_color)
    mask = np.all(diff <= 20, axis=-1)
    image[mask] = [255, 255, 255]

    return image


# 보더 추가
def f_add_border_lines(image):
    lower_color = np.array([230, 230, 230])
    upper_color = np.array([230, 230, 230])
    mask = cv2.inRange(image, lower_color, upper_color)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    border_thickness = 2
    border_color = (0, 0, 0) 

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w >= 1000: 
            cv2.rectangle(image, (x, y), (x + w, y + h), border_color, border_thickness)

    return image


# PDF TO Image
def f_convert_pdf_to_images(pdf_path, output_dir):
    pdf_document = fitz.open(pdf_path)

    os.makedirs(output_dir, exist_ok=True)
    print(output_dir)

    image_paths = []

    for page_number in range(pdf_document.page_count-1): # 마지막 페이지 제외(요약)
        page = pdf_document[page_number]
        pixmap = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))  # DPI

        image_path = os.path.join(output_dir, f"page_{page_number + 1}.png")
        pixmap.save(image_path, "png")
        image_paths.append(image_path)

        print(f">> Page {page_number + 1} converted to image: {image_path}")

    return image_paths, pdf_document, page_number 


# 문자열 제외
def filter_characters(input_string, exclude_list):
    # 제외 (워터마크 문자 조합)
    # "열람용" 기본리스트. 예외 발생시 추가하여 사용
    # characters_to_exclude = ['열\n', '열 \n', '람\n', '람 \n', '용\n', '용 \n', '열 람\n', '열 람 \n', '람 용\n', '람 용 \n', '열 람 용\n', '열 람 용 \n', '열람\n', '열람 \n', '람용\n', '람용 \n', '열람용\n', '열람용 \n']

    # 전체 예외리스트 받아서 사용
    characters_to_exclude = []
    characters_to_exclude += exclude_list
    # 제외 문자 패턴을 정규 표현식으로 생성
    pattern = '|'.join(map(re.escape, characters_to_exclude))
    # 문자 제거
    filtered_string = re.sub(pattern, '', input_string)

    return filtered_string


# json 형식 반환
def main(input_path, exclude_list):

    dir_path, name_extension, pdf_name = path_parse(input_path)
    out_path = dir_path + "/" + pdf_name

    image_paths, pdf_document, page_number = f_convert_pdf_to_images(input_path, out_path)

    total_data_list = []

    for page_number, image_path in enumerate(image_paths, start=0):

        image = util.utf_imread(image_path)
        
        image_height, image_width, _ = image.shape

        # precessed_image = f_image_preocessing(image)

        added_border_image = f_add_border_lines(image)

        watermark_color_1 = (213, 213, 213)  # D5D5D5
        watermark_color_2 = (224, 224, 224)  # E0E0E0

        removed_watermark_image = f_remove_watermark(added_border_image, watermark_color_1)
        removed_watermark_image = f_remove_watermark(removed_watermark_image, watermark_color_2)

        gray_image = cv2.cvtColor(removed_watermark_image, cv2.COLOR_BGR2GRAY)

        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

        _, thresholded_image = cv2.threshold(blurred_image, 200, 255, cv2.THRESH_BINARY)

        edges = cv2.Canny(thresholded_image, threshold1=50, threshold2=150)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        tables = []

        line_image = image.copy()

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 1000 and h > 100: 
                tables.append((x, y, w, h))

        tables.reverse()

        pdf_page = pdf_document[page_number]

        pdf_page_width = pdf_page.rect.width
        pdf_page_height = pdf_page.rect.height


        for table_number, (x, y, w, h) in enumerate(tables, start=1):

            if table_number == 1:
                new_list = []

            roi = thresholded_image[y:y + h, x:x + w]
            cell_contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            cell_number = 1

            cell_rows = {}

            cell_contours = sorted(cell_contours, key=lambda c: cv2.boundingRect(c)[1])

            for idx, contour in enumerate(cell_contours):
                x_cell, y_cell, w_cell, h_cell = cv2.boundingRect(contour)
                x_global, y_global = x + x_cell, y + y_cell

                if w == w_cell or h == h_cell or w_cell <= 10 or h_cell <= 10:
                    continue

                cv2.rectangle(line_image, (x_global, y_global), (x_global + w_cell, y_global + h_cell), (0, 255, 0), 2)
                cv2.putText(line_image, f"[T_{table_number} C_{cell_number}]", (x_global + w_cell // 2, y_global + h_cell // 2), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)

                pdf_x1 = x_global * (pdf_page_width / image_width)
                pdf_y1 = y_global * (pdf_page_height / image_height)
                pdf_x2 = (x_global + w_cell) * (pdf_page_width / image_width)
                pdf_y2 = (y_global + h_cell) * (pdf_page_height / image_height)

                text = pdf_page.get_text("text", clip=(pdf_x1, pdf_y1, pdf_x2, pdf_y2))

                exclude_list = exclude_list
                text = filter_characters(text, exclude_list) # 텍스트 필터링

                if y_global not in cell_rows:
                    cell_rows[y_global] = []
                cell_rows[y_global].append({
                    "x": x_global,
                    "y": y_global,
                    "width": w_cell,
                    "height": h_cell,
                    "text": text.strip()
                })

                cell_number += 1

                if idx == 0:
                    new_list = []

                # row 처리 (row, columns)
                new_list = util.f_group_list(list(cell_rows.values()))

            data_list = []

            # 박스 값이 역순이라 정순으로 변경
            for idx, group in enumerate(new_list):
                
                # 좌표값 같이 처리
                for sublist in group:
                    reversed_dict_list = list(reversed(sublist))  # 리스트를 뒤집음
                    row_length = len(reversed_dict_list[0])
                    grouped_values = [list(reversed_dict_list[i:i + row_length]) for i in range(0, len(reversed_dict_list), row_length)]
                    data_list.append({"row": str(idx), "columns": grouped_values})

                '''
                # 기존 텍스트만 처리
                text_values = [item["text"] for row in group for item in row]
                row_length = len(group[0])
                grouped_text_values = [list(reversed(text_values[i:i + row_length])) for i in range(0, len(text_values), row_length)]
                data_list.append({"row": str(idx), "columns": grouped_text_values})
                # print(type(data_list))
                '''

            '''
            # 하나씩 JSON 형식으로 변환해서 보여주는 용도
            json_data = json.dumps(data_list, indent=4, ensure_ascii=False)
            print(json_data)
            '''

            total_data_list.append(data_list)

        image = None
        f_make_processed_img(out_path, page_number, line_image) # 이미지 생성 처리


    # 세로 처리 2023.10.06 (row, columns)
    total_data_list = merge.f_colspan(total_data_list)

    # 가로 처리 2023.10.08 (row, columns)
    total_data_list = merge.f_rowspan(total_data_list)


    # 그룹 처리 (row, columns)
    data = group_parser.refineHeader(total_data_list)
    data = group_parser.recoverType1(data)
    data = group_parser.recoverType2(data)
    #data = recoverType3(data)
    total_data_list = group_parser.refineData(data)


    # 형식변환 (key, value)
    total_data_list = util.f_format_conversion(total_data_list)

    # 추가 데이터 (집합건물 고유번호 열람일시 관할등기소 key, value))
    all_text = plus_data.getAllData(input_path)
    add_data = plus_data.textParser(all_text)
    if total_data_list:
        total_data_list.insert(0, add_data)
    else:
        total_data_list.append(add_data) 

    # JSON 형식 변환
    json_data_combined = json.dumps(total_data_list, indent=4, ensure_ascii=False)
    # print(json_data_combined)

    # Json 파일 생성 처리
    f_make_json_file(json_data_combined, out_path, pdf_name) 

    pdf_document.close()

    return total_data_list


# 이미지 파일 생성
def f_make_processed_img(output_dir, page_number, processed_image):
    line_image_path = os.path.join(output_dir, f"p_image_{page_number + 1}.png")
    util.utf_imwrite(line_image_path, processed_image)
    print(f">>> Processed image for page {page_number + 1} saved to {line_image_path}")


# JSON 파일 생성
def f_make_json_file(data, output_dir, pdf_name):
    output_path = output_dir + "/" + pdf_name + ".json"
    with open(output_path, "w", encoding="utf-8") as combined_output_file:
        combined_output_file.write(data)
    print(">>> JSON data saved to", output_path)


# 필요없는 디렉터리 삭제 처리(필요 시 사용)
def f_delete_directory(path):
    try:
        shutil.rmtree(path)
        print(f">> Removed directory : {path} ")
    except Exception as e:
        print(f">> Error removing directory: {str(e)}")


# PDF 파일 맞는지 확인        
def is_valid_pdf(file_path):
    file_extension = os.path.splitext(file_path)[-1].lower()

    return file_extension == '.pdf'


# 경로 파싱
def path_parse(input_pdf_path):
    dir_path, name_extension = os.path.split(input_pdf_path)
    name, _ = os.path.splitext(name_extension)

    # 'C:\\바탕 화면\\프로젝트\\pdf처리\\자료\\등기부등본모음', '빌라등기4_광진구.pdf', '빌라등기4_광진구'
    return dir_path, name_extension, name


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract tables from PDF files To JSON data")
    parser.add_argument("-i", "--input", required=True, help="Input PDF file path")
    args = parser.parse_args()

    input_path = args.input

    exclude_list = []

    if not is_valid_pdf(input_path):
        print("Input file is not a valid PDF file.")
    else:
        main(input_path, exclude_list)
