#list data
import data
import math
import random

MAX = 7
MIN = 5

def members(list) :
    # 값 검증
    if MAX == MIN and len(list) % MAX != 0 :
        print("그룹을 생성할 수 없습니다. (조건에 맞지않는 조직생성)")
        return []
    elif MAX < MIN :
        print("최소값이 최댓값보다 큽니다.")
        return []
    #로직 시작
    membersGroup = []
    resultData = {}
    random.shuffle(list)   #리스트 섞음
    for i in range(0, math.trunc(len(list) / MAX)) : #소수값제거, 정수만 반환하도록
        membersGroup.append(MAX)
    leftData = len(list) - sum(membersGroup)
    while leftData != 0 :
        if MIN <= (leftData % MAX) <= MAX :
            membersGroup.append(leftData)
            leftData = leftData - (leftData % MAX)
        elif leftData < MIN :
            del membersGroup[-1]
            leftData = leftData + MAX
        else :
            membersGroup.insert(0, MIN)
            leftData = leftData - MIN

    membersGroup.sort(reverse=True)   #내림차순으로 정렬
    print(membersGroup)
    print(sum(membersGroup))
    for index, data in enumerate(membersGroup) :
        resultData[str(index+1) + '조'] = list[0:data]   #1조,2조,3조 순
        del list[0:data]

    return resultData



print(members(data.list))


