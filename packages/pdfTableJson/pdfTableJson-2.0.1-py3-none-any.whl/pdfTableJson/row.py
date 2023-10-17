import json
import util

def f_rowspan(data):
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>f_rowspan 시작")

    before_columns = None
    total_list = []

    for table in data:

        for group in table:
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
                        total_list.pop(-1)
                        total_list.append(result_list)


                # 초기 반복에서 이전 columns를 설정
                before_columns = current_columns

            # 체크인 경우, 한번에 이전이후 값 처리, 추가하지 않음
            if not check:
                total_list.extend(text_values)
                

    # 그룹처리
    temp_list = util.f_group_list(total_list)
    # row, columns 처리
    total_list = []
    for sub in temp_list:
        total_list.append([{"row:" : str(0), "columns": sub}])

    #total_list = json.dumps(total_list, indent=4, ensure_ascii=False)
    #print(total_list)
    
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>f_rowspan 종료")
    return total_list
