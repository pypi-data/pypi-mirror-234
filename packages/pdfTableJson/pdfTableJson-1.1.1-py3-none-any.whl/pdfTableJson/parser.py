import json
import re

#file = open('/content/drive/MyDrive/PDF/아파트등기3_중랑구-2.json')
#file = open('/content/drive/MyDrive/PDF/빌라등기1_강남구-2.json')
#file = open('/content/drive/MyDrive/PDF/아파트등기2_용산구-2.json')
# file = open('/content/drive/MyDrive/PDF/빌라등기5_송파구-2.json')
# data = json.load(file)
# file.close()

"""
헤더부분이 2개의 그룹으로 나눠져 있는 경우 하나로 처리
['일련번호', '부동산에 관한 권리의 표시', '관할등기소명', '순위번호', '기 타 사 항']
['생성원인', '변경/소멸']
TO
['일련번호', '부동산에 관한 권리의 표시', '관할등기소명', '순위번호', '생성원인', '변경/소멸']
"""
def refineHeader(data):
  # column 내용이 '생성원인' 찾기
  for table in data:
    idxGroup = 0
    for group in table:
      columns = group['columns'][0]
      print(columns)
      if re.match('생성원인',columns[0]) != None:
        print(f"\t<<<헤더처리대상>>> {columns}")
        beforeColumns = table[idxGroup - 1]['columns'][0]
        # '기 타 사 항' 삭제
        beforeColumns.pop()
        # '생성원인', '변경/소멸' 추가
        beforeColumns.extend(columns)
        # '생성원인', '변경/소멸' 삭제
        columns.pop()
        columns.pop()
        # 삭제대상그룹설정
        columns.append('')
        print(f"\t헤더처리 {beforeColumns}")

      idxGroup += 1

  # 빈그룹삭제처리
  for table in data:
    idxGroup = 0
    for group in table:
      # 비여있는 group은 삭제
      if len(group['columns']) == 1 and group['columns'][0][0] == '':
        del(table[idxGroup])

      idxGroup += 1

  return data

"""
헤더만 있는 그룹 삭제 및 헤더없는 그룹 이전그룹과 머지
"""
def refineData(data):
  # 헤더없는 데이타 그룹 헤더와 병합
  for table in data:
    idxGroup = 0
    for group in table:
      columns = group['columns']
      if re.match('(표시번호|순위번호|일련번호|목록번호)',columns[0][0]) == None and re.match('.+ (표  제  부|대지권의 목적인 토지의 표시|갑      구|을      구|대지권의 표시|공동담보목록) .+',columns[0][0]) == None:
        print(f"<<<헤더병합대상>>> {columns}")
        table[idxGroup - 1]['columns'].extend(columns)
        # 병합그룹삭제
        del(table[idxGroup])

      idxGroup += 1

  # 헤더만 있는 그룹 삭제
  for table in data:
    idxGroup = 0
    for group in table:
      columns = group['columns']
      if len(columns) == 1 and re.match('(표시번호|순위번호|일련번호)',columns[0][0]) != None:
        print(f"<<<헤더삭제대상>>> {columns}")
        # 그룹삭제
        del(table[idxGroup])

      idxGroup += 1

  return data

"""
type1 처리 (대분류가 아닌데 내용이 1개의 컬럼이면 처리대상)
"""
def recoverType1(data):
  print(f'recoverType1 table count: {len(data)}')
  for idxTable in range(0,len(data)):
    print('----------------------------------------------------------------------------------------------------------')
    print(f'table: {idxTable} group count: {len(data[idxTable])}')
    print('----------------------------------------------------------------------------------------------------------')
    for idxGroup in range(0,len(data[idxTable])):
      group = data[idxTable][idxGroup]
      #print(f"group: {row['row']} columns count: {len(row['columns'])}")
      columns = group['columns']
      if len(columns[0]) == 1:
        # 내용이 1컬럼이면 대상
        value = columns[0][0]
        # 내용의 첫번째 필드값이 지정된 테이블 내용(표제부,대지권의목적인토지의표시,갑구을구 등)이 아니면 대상
        if re.match('.+ (표  제  부|대지권의 목적인 토지의 표시|갑      구|을      구|대지권의 표시|공동담보목록) .+', value) == None:
          print(f"\t<<<처리대상1>>> {value}")
          beforeRow = data[idxTable][idxGroup - 1]
          beforeColumns = beforeRow['columns'][len(beforeRow['columns']) - 1]
          print(f'\t병합대상 BEFORE {beforeColumns}')
          beforeColumns[len(beforeColumns) - 1] = beforeColumns[len(beforeColumns) - 1] + '\n@' + value + '@'
          print(f'\t병합대상 AFTER {beforeColumns}')
          # 처리 후 대상 내용 삭제
          if len(columns) > 1:
            columns[0] = ['']
          else:
            columns[0] = ''
      print(columns)

  # 빈그룹삭제처리
  for table in data:
    idxGroup = 0
    for group in table:
      # 비여있는 group은 삭제
      if len(group['columns']) == 1 and group['columns'][0] == '':
        #print(f"삭제대상 {group}")
        del(table[idxGroup])
      else:
        idxColumn = 0
        for column in group['columns']:
          if len(column) == 1 and column[0] == '':
            #print(f"삭제대상 {column}")
            del(group['columns'][idxColumn])
          idxColumn += 1

      idxGroup += 1

  return data

"""
type2 처리 (데이터item의 첫번째 필드가 공백이면 처리대상)
"""
def recoverType2(data):
  print(f'recoverType2 table count: {len(data)}')
  for idxTable in range(0,len(data)):
    print('----------------------------------------------------------------------------------------------------------')
    print(f'table: {idxTable} group count: {len(data[idxTable])}')
    print('----------------------------------------------------------------------------------------------------------')
    for idxGroup in range(0,len(data[idxTable])):
      group = data[idxTable][idxGroup]
      #print(f"group: {row['row']} columns count: {len(group['columns'])}")
      columns = group['columns']
      if len(columns) != 1:
        # Header(!=None)가 아니면서 첫번째 필드가 공백이면('') 이전 group동일 필드와 합침
        idx = 0
        if re.match('(표시번호|순위번호|일련번호)',columns[0][0]) != None:
          idx = 1

        for v in range(idx,len(columns)):
          if columns[v][0] == '':
            print(f"\t<<<처리대상2>>> {columns[v]}")
            tmpIdxTable = idxTable
            tmpIdxGroup = idxGroup - 1
            print()
            if idxGroup == 0 or re.match('(표시번호|순위번호|일련번호)',data[tmpIdxTable][tmpIdxGroup]['columns'][0][0]) != None:
              tmpIdxTable = tmpIdxTable - 1
              tmpIdxGroup = len(data[tmpIdxTable]) - 1
            beforeRow = data[tmpIdxTable][tmpIdxGroup]
            beforeColumns = beforeRow['columns'][len(beforeRow['columns']) - 1]
            print(f'\t병합대상 BEFORE {beforeColumns}')
            for v2 in range(0,len(beforeColumns)):
              if columns[v][v2] != '':
                beforeColumns[v2] = beforeColumns[v2] + '\n@' + columns[v][v2] + '@'
            print(f'\t병합대상 AFTER {beforeColumns}')
            # 삭제대상
            columns[v] = ['']

      print(columns)

  # 빈그룹삭제처리
  for table in data:
    for group in table:
      idxGroup = 0
      for column in group['columns']:
        #print(column)
        if len(column) == 1 and column[0] == '':
          print(f"삭제대상 {column}")
          del(group['columns'][idxGroup])

        idxGroup += 1

  return data

"""
type3 처리 (데이타 item의 첫번째 필드가 공백이면 처리대상)
"""
def recoverType3(data):
  print(f'recoverType3 table count: {len(data)}')
  for idxTable in range(0,len(data)):
    print('----------------------------------------------------------------------------------------------------------')
    print(f'table: {idxTable} group count: {len(data[idxTable])}')
    print('----------------------------------------------------------------------------------------------------------')
    for idxGroup in range(0,len(data[idxTable])):
      group = data[idxTable][idxGroup]
      columns = group['columns']
      if len(columns) != 1:
        # Header(!=None)가 아니면서 첫번째 필드가 공백이면('') 이전 group동일 필드와 합침
        idx = 0
        if re.match('(일련번호)',columns[0][0]) != None:
          idx2 = 1

        for v in range(idx,len(columns)):
          if columns[v][0] == '':
            print(f"\t<<<처리대상3>>> {columns[v]}")
            tmpIdxTable = idxTable
            tmpIdxGroup = idxGroup - 1
            if idxGroup == 0:
              tmpIdxTable = tmpIdxTable - 1
              tmpIdxGroup = len(data[tmpIdxTable]) - 1
            beforeRow = data[tmpIdxTable][tmpIdxGroup]
            beforeColumns = beforeRow['columns'][len(beforeRow['columns']) - 1]
            print(f'\t병합대상 BEFORE {beforeColumns}')
            for v2 in range(0,len(beforeColumns)):
              if columns[v][v2] != '':
                beforeColumns[v2] = beforeColumns[v2] + '\n@' + columns[v][v2] + '@'
            print(f'\t병합대상 AFTER {beforeColumns}')
            # 삭제대상
            columns[v] = ['']

      print(columns)

  # 빈그룹삭제처리
  for table in data:
    for group in table:
      idxGroup = 0
      for column in group['columns']:
        #print(column)
        if len(column) == 1 and column[0] == '':
          print(f"삭제대상 {column}")
          del(group['columns'][idxGroup])

        idxGroup += 1

  return data

'''
for table in data:
  for group in table:
    print(group)
'''