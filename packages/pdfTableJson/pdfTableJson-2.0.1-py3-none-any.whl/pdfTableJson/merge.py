import json
try:
    from . import util  # package # utf-8 # pypi
except ImportError:
    import util  # package # utf-8 # local

# columns[0] (header) 에서 세로로 나뉜 경우 처리
# 첫번째 columns의 0번인덱스의 height 값과, 나머지 인덱스들의 height 값을 비교하여, 다른 값이 있는경우 세로로 나뉜것으로 추측
'''
['일련번호', '부동산에 관한 권리의 표시', '관할등기소명', '순위번호', '기 타 사 항']
['생성원인', '변경/소멸']
TO
['일련번호', '부동산에 관한 권리의 표시', '관할등기소명', '순위번호', '생성원인', '변경/소멸']
''' 
def f_colspan(data):
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


    return total_list



# 데이터에서 가로로 나뉜 경우 처리
# 위 그룹이 아래 그룹보다 셀의 개수가 많고, width 값 같은 것 기준
# 윗 그룹의 마지막 column의 값에 연결, "@" 구분자
'''
[2, 소유권이전, 2020, 2020, 공유자]
[1번신탁등기말소, '', 신탁재산의 귀속, '']
TO
[2, 소유권이전@1번신탁등기말소, 2020@, 2020@신탁재산의 귀속, 공유자@]
'''
def f_rowspan(data):
    before_columns = None
    total_list = []

    for item in data:

        temp_list = []

        for group in item:

            check = False

            current_columns = group['columns']

            # 전체 데이터, 텍스트만 추출
            text_values = []
            for group in current_columns:
                t = []
                for item in group:
                    t.append(item['text'])
                text_values.append(t)
            #total_list.extend(text_values)

            if before_columns is None:
                before_columns = current_columns
            else:
                # 이전로우보다 작은 현재로우가 대상, width 값으로 확인
                if len(before_columns[0]) > len(current_columns[0]):

                    before_width = [item['width'] for item in before_columns[0]]
                    current_width = [item['width'] for item in current_columns[0]]

                    # 일치하는 width 값 있는지 확인해서, 인덱스 indices 저장
                    indices = []
                    # before_width 이미 사용된 인덱스를 저장할 집합
                    used_indices = set()
                    # current_width 순서대로 읽으면서 before_width 일치하는 값을 찾고 인덱스를 저장
                    for item in current_width:
                        for index, value in enumerate(before_width):
                            # 이미 사용된 인덱스인지 확인하고 사용되지 않았으면 저장
                            if index not in used_indices and item == value:
                                indices.append(index)
                                used_indices.add(index)
                    # print(indices)

                    # indices 비어있지 않은 경우 처리
                    # 이전 컬럼의 마지막 리스트의 텍스트 값에 현재 컬럼의 텍스트 값을 연결
                    if len(indices) != 0:
                        check = True

                        last_list = before_columns[-1]  # 이전칼럼의, 마지막 리스트 선택
                        A = [item['text'] for item in last_list]  
                        b_list = current_columns[0] # 현재 리스트
                        B = [item['text'] for item in b_list]  

                        # 결과를 저장할 빈 리스트를 생성합니다.
                        result_list = A[:]  # A 리스트를 복사하여 result_list 초기화
                        for i in range(len(indices)):
                            a_index = indices[i]
                            b_index = i
                            result_list[a_index] += "@" + B[b_index]

                        # print(f"---- {result_list}")
                        # 이전값(나뉜대상값) 삭제, 붙여서 한번에 처리
                        temp_list.pop(-1)
                        temp_list.append(result_list)


                # 초기 반복에서 이전 columns를 설정
                before_columns = current_columns

            # 체크인 경우, 한번에 이전이후 값 처리, 추가하지 않음
            if not check:
                temp_list.extend(text_values)
                

        # 그룹처리
        temp_list = util.f_group_list(temp_list)
        # row, columns 처리
        data_list = []
        for sub in temp_list:
            data_list.append({"row:" : str(0), "columns": sub})

        # 합치기
        total_list.append(data_list)

    # total_list = json.dumps(total_list, indent=4, ensure_ascii=False)
    # print(total_list)
    

    return total_list
