import numpy as np
import cv2
import os

# imread, imwrite utf-8 
def utf_imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None


# imread, imwrite utf-8 
def utf_imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


# 그룹 처리
# 개수 기준으로 그룹으로 묶는 용도
def f_group_list(input_list):
    
    result_list = []
    current_group = []
    prev_length = None

    for item in input_list:
        current_length = len(item)

        if prev_length is None:
            prev_length = current_length
            current_group = [item]
        elif prev_length == current_length:
            current_group.append(item)
        else:
            result_list.append(current_group)
            current_group = [item]
            prev_length = current_length

    if current_group:
        result_list.append(current_group)

    return result_list


# 형식 변환
# row, columns 형식에서, key:value 형식으로 변환
def f_format_conversion(total_data_list):

    final_result = []  # 최종 결과를 저장할 리스트

    for data in total_data_list:
        
        # 모든 아이템에서 'columns' 값을 추출
        all_columns = [item['columns'] for item in data]

        for item in all_columns:
            if item and len(item) > 0:
                
                if len(item) == 1:
                    # 한 줄 짜리 처리
                    result = [{'th': data for data in item}]
                    #print(result)
                    final_result.extend(result)
                else:
                    # 기본 처리
                    result = []
                    # 첫 번째 리스트를 헤더로 사용
                    header = item[0]
                    # 나머지 리스트를 순회하면서 딕셔너리로 변환
                    for item in item[1:]:
                        data_dict = {}
                        for i, value in enumerate(item):
                            key = header[i]  # 헤더의 열 이름을 키로 사용
                            data_dict[key] = value
                        result.append(data_dict)
                    final_result.extend(result)

    return final_result
