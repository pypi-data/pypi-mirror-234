from ..outerIO  import dart
from ..common   import conf, dataProc
from ..outerIO  import ebest    as eb
import pandas as pd


def SyncCmpnyList():

    filePathNm = conf.companyInfoPath + "/기업list(금감원).pkl"

    dfData = dart.GetCmpnyList()

    dataProc.WritePickleFile(filePathNm, dfData) 


def SyncCmpnyAcntInfo(year, quarter, selectToc = 5, currentPageSize = 100):
    
    filePathNm = conf.companyInfoPath + "/기업list(금감원).pkl"    
    stockItemList = dataProc.ReadPickleFile(filePathNm)    


    filePathNm = conf.companyInfoPath + "/재무정보(금감원).pkl"

    # selectToc : 0 (연결재무제표), 5(재무제표)    
    df = dart.GetCmpnyAcntInfo(year, quarter, selectToc=selectToc, currentPageSize=currentPageSize)

    resData = df.values.tolist()
    columns = df.columns.tolist()

    # print(resData)

    # 기존 데이터 read
    currData = dataProc.ReadPickleFile(filePathNm)

    if not currData.get('data'):
        currData['data'] = {}   

    # columns
    # '종목명', '결산월', 
    # '기준년도', '기준분기', '보고서종류'
    # '유동자산','비유동자산','자산총계','유동부채','비유동부채','부채총계','자본금','이익잉여금','자본총계',
    # '매출액','영업이익','세전이익','당기순이익'

    currData['columns'] = columns[2:] + ['매출액_분기','영업이익_분기','세전이익_분기','당기순이익_분기']

    for idx in range(len(resData)):
        title = resData[idx][0]

        shCode = stockItemList[stockItemList['회사명']==title]['종목코드'].values[0]

        if not currData['data'].get(shCode):
            currData['data'][shCode] = {}
        if not currData['data'][shCode].get('info'):
            currData['data'][shCode]['info'] = []
        currData['data'][shCode]['종목명'] = title
        currData['data'][shCode]['결산월'] = resData[idx][1]
               
        tmpData = dataProc._MergeData(currData['data'][shCode]['info'], [resData[idx][2:] + [0,0,0,0]], sortCols=2)
        # columns
        # '기준년도', '기준분기', '보고서종류'
        # '유동자산','비유동자산','자산총계','유동부채','비유동부채','부채총계','자본금','이익잉여금','자본총계',
        # '매출액','영업이익','세전이익','당기순이익'
        # '매출액_분기','영업이익_분기','세전이익_분기','당기순이익_분기'

        for i in range(len(tmpData)):
            # 매출액(12번째)
            for x in [12,13,14,15]:  # 위치 12번째: 매출액, 13:당기순이익, 14:영업이익, 15:세전이익
                if (i == 0 and tmpData[i][2] != '1분기'):
                    continue
                elif tmpData[i][2] == '1분기':
                    if tmpData[i][x] != '':
                        tmpData[i][x+4] = tmpData[i][x]
                else:
                    if tmpData[i][x] != '' and tmpData[i-1][x] != '' :
                        tmpData[i][x+4] = tmpData[i][x] - tmpData[i-1][x]

        currData['data'][shCode]['info'] = tmpData

    dataProc.WritePickleFile(filePathNm, currData) 
