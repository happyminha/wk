# 헤더 설정
from enum import Enum
import operator


# 해당 데이터의 index 값 얻기 ( 여러개 있을시 여러개 출력 )
def all_indices(value, qlist):
    indices = []
    idx = -1
    while True:
        try:
            idx = qlist.index(value, idx + 1)
            indices.append(idx)
        except ValueError:
            break
    return indices


# 일자 형태 (변경이 없으므로 enum 설정)
class WEEK(Enum):
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4


# 최대 일할수 있는 범위 지정
PARTTIMER = {'a_time': 10, 'b_time': 10, 'c_time': 10, 'd_time': 10}

# 기본적으로 일할수 있는 시간 범위 지정
woringHour = [10, 11, 12, 13, 14, 15, 16, 17, 18]


def make_timetable(a_time: list, b_time: list, c_time: list, d_time: list):
    # 데이터 할당
    allData = {}
    allData['a_time'] = a_time
    allData['b_time'] = b_time
    allData['c_time'] = c_time
    allData['d_time'] = d_time

    # 일자 데이터 범위별로 추출
    for key, value in allData.items():
        date = {}
        for i, d in enumerate(value):
            splitTime = d.split(';')
            date[WEEK(i).name] = []
            for j in splitTime:
                date[WEEK(i).name].append(
                    list(range(int(j.split('~')[0].split(':')[0]), int(j.split('~')[1].split(':')[0]) + 1)))
        allData[key] = date

    # 결과를 추출하기 위한 dict 형태의 데이터 생성
    tempresult = {}
    result = {}
    WEEKTIME = {}
    for i in WEEK:
        WEEKTIME[i.name] = woringHour
        tempresult[i.name] = {}
        result[i.name] = {}
        for hour in woringHour:
            tempresult[i.name][str(hour)] = []
            result[i.name][str(hour)] = []

    # 일자별 , 시간별 일할수 있는 사람으로 데이터 전처리 수행
    # ex ) MON : 10 : [a근무자, b근무자]
    for day, allhour in WEEKTIME.items():
        for hour in allhour:
            for worker, wanttime in allData.items():
                for workday, times in wanttime.items():
                    for time in times:
                        if day == workday and len(all_indices(hour, time)) > 0:
                            tempresult[day][str(hour)].append(worker)

    # 해당시간에만 근무할수 있는 작업자부터 할당
    for day, rdata in tempresult.items():
        for hour, data in rdata.items():
            if len(data) == 1 and PARTTIMER[data[0]] > 0:
                result[day][hour] = data[0]
                PARTTIMER[data[0]] = PARTTIMER[data[0]] - 1
            else:
                result[day][hour] = {}
                for i in data:
                    result[day][hour][i] = PARTTIMER[i]

    # 근무시간이 겹치면 가장 많이 일할수 있는 사람 부터 배치
    for day, rdata in result.items():
        for hour, data in rdata.items():
            if type(data) == dict:
                if len(data) > 0:
                    maxkey = max(data.items(), key=operator.itemgetter(1))[0]
                    if PARTTIMER[maxkey] > 0:
                        result[day][hour] = maxkey
                        PARTTIMER[maxkey] = PARTTIMER[maxkey] - 1
                    else:
                        result[day][hour] = "10시간 초과"
                else:
                    result[day][hour] = "근무자 없음"

    print("남은 근무시간 : ")
    print(PARTTIMER)

    print("시간표 : ")
    for days, datas in result.items():
        print(days)
        print("====================================================================================")
        for hour, worker in datas.items():
            print(str(hour) + "시 : ", end="")
            print(worker, end="\t | ")
        print("\n==================================================================================")


# 지정된 데이터
a_time = ['10:00~14:00', '15:00~18:00', '11:00~13:00;14:00~16:00', '10:00~11:00', '15:00~18:00']
b_time = ['11:00~14:00', '14:00~16:00', '16:00~18:00', '10:00~11:00;12:00~13:00', '14:00~16:00']
c_time = ['14:00~16:00', '16:00~18:00', '10:00~12:00', '12:00~14:00', '14:00~16:00']
d_time = ['14:00~18:00', '10:00~18:00', '12:00~14:00', '14:00~15:00;16:00~17:00', '10:00~12:00']

# 함수호출
make_timetable(a_time, b_time, c_time, d_time)