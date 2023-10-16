import json
import util

def f_colspan(data):
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>f_colspan 시작")

    cnt = 0 
    total_list = []
    for item in data:

        check_list = []
        current_row = None
        before_column = None

        temp_list = []

        for entry in item:
            row = entry.get("row")
            columns = entry.get("columns")

            temp = []
            # row 변경 부분
            if row != current_row:
                current_row = row

                if((columns and len(columns) > 0) and (len(check_list)==0)):
                    check = False
                    before_column = columns[0]

                    # 각 그룹이되는 row의 첫번째 columns의 값 : first_column_value
                    first_column_value = columns[0]

                    # 첫번째 columns 의 height 값들을 비교하여 첫번째 height값과 다른 값을 가진 
                    # 셀의 인덱스값을 check_list에 저장, 동일 row에 다른 값들과 다른 height를 가지는 것
                    # "기타사항"
                    height_values = [entry['height'] for entry in first_column_value]
                    first_height_values = height_values[0]
                    check_list =  [i for i, value in enumerate(height_values) if value != first_height_values]

                    res = [item for sublist in columns for item in sublist]
                    # res = [item['text'] for item in res] # 텍스트만 추출
                    # print(res)
                    
                else:
                    check = True
                    # 분기점이 존재했다는 것
                    #print(f"before_column : {before_column}")
                    #print(f"columns[0] : {columns[0]}")
                    # 그다음 값은 해당 분기점에서 나뉘어져 나온 th값이 됨
                    # "생성원인, 변경/소멸"
                    for index in check_list:
                        del before_column[index]
                        before_column[index:index] = columns[0]
                        res = before_column
                        # res = [item['text'] for item in before_column] # 텍스트만 추출
                        # print(res)

                    check_list=[]
                    
                temp.append(res)

            else :
                check = False
                # 같은 row 데이터
                res = [item for sublist in columns for item in sublist]
                # res = [item['text'] for item in res] # 텍스트만 추출
                # print(res)

                temp.append(res)

            
            # 분기점 있었을 경우 이전 추가했던 값 제거 (분기점에서 이전 값까지 합쳐서 출력함)
            if check:
                temp_list.pop()

            temp_list.extend(temp)

        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")    
        # print(temp_list)

        # 그룹처리
        temp_list = util.f_group_list(temp_list)
        # row, columns 처리
        data_list = []
        for sub in temp_list:
            data_list.append({"row:" : str(cnt), "columns": sub})
        # 합치기
        total_list.append(data_list)

        cnt += 1    


    #total_list = json.dumps(total_list, indent=4, ensure_ascii=False)
    #print(total_list)

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>f_colspan 종료")

    return total_list

