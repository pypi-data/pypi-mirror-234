# from   ..common   import conf, dataProc
from ..outerIO  import kind
from ..common   import conf, dataProc
from ..innerIO  import stockInfo  as sd
import pandas   as pd
import datetime 

def SynchDailyStockTradeInfo(sDate, eDate):

    print('\r' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ': 데이터 추출 시작')    
    
    # tradeList = []
    
    # curDt = sDate
    # while curDt <= eDate:
    #     df = kind.GetStockTradeInfo(curDt)    
    #     columns = df.columns.tolist()    
    #     tradeList += df.values.tolist()
            
    #     curDt = (datetime.datetime.strptime(curDt, "%Y%m%d") + datetime.timedelta(days=1)).strftime("%Y%m%d")     
    df = pd.DataFrame([])
    for x in pd.date_range(sDate, eDate):        
            
        if (x.weekday() in (5, 6) or   # 토요일/일요일
            datetime.datetime.strftime(x, '%m%d') in ('0101', '0301', '0505', '0606', '0815', '1003', '1225' ) or 
            datetime.datetime.strftime(x, '%m%d') == '1009' and datetime.datetime.strftime(x, '%Y') >= '2013' ):  # 법정공휴일
            pass
        else:
            cDate = datetime.datetime.strftime(x, '%Y%m%d')            
            df = pd.concat([df, kind.GetStockTradeInfo(cDate)])            
        
    print('\n' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ': 데이터 저장 시작')   
    # df = pd.DataFrame(tradeList, columns=columns)
    # df = df[df['시가']!='-']

    shCodeList = sorted(df['종목코드'].unique())
    for i, shCode in enumerate(shCodeList):
        # # 파일에 저장
        sd._SaveStockTrade(shCode, df[df['종목코드']==shCode][['일자', '시가', '고가', '저가', '종가', '거래량', '거래대금']].values.tolist() )    

        print('\r' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ': 전체대상(' + str(len(shCodeList)) + '), 완료(' + str((i+1)) + '), 종목코드('  + shCode + ')', end='')            
    
    print('\n' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ' 데이터 저장 완료')   

# def SynchDailyStockTradeInfo(sDate, eDate):

#     curDt = sDate
#     while curDt <= eDate:
#         x, columns = kind.GetStockTradeInfo(curDt)
#         df = pd.DataFrame(x, columns=columns)
#         df = df[df['시가']!='-']

#         if len(df) > 0:
#             print('')
#             for i in range(len(df)):
#                 # # 파일에 저장
#                 sd._SaveStockTrade('일별주가', df['종목코드'].iloc[i], [df[['일자', '시가', '고가', '저가', '종가', '거래량', '거래대금']].iloc[i].tolist()])    

#                 print('\r' + curDt, (i+1), '/',  len(df), end='')
#             curDt = (datetime.datetime.strptime(curDt, "%Y%m%d") + datetime.timedelta(days=1)).strftime("%Y%m%d")     
#             print(' 완료')

def SyncDividendInfo(sYear, eYear, currentPageSize = 100, marketType='', settlementMonth='', selYearCnt = 3):
    filePathNm = conf.companyInfoPath + "/주식배당정보(한국거래소).pkl"

    for selYear in range(eYear, sYear-1, -1*selYearCnt):
        if selYear >= (sYear + selYearCnt):
            print(selYear, selYearCnt)
            yearCnt = selYearCnt
        else:
            print(selYear, selYear - sYear + 1)
            yearCnt = selYear - sYear + 1

        df = kind.GetDividendInfo(selYear, currentPageSize, marketType, settlementMonth, yearCnt)

        resData = df.values.tolist()
        columns = df.columns.tolist()[2:]

        # 기존 데이터 read
        currData = dataProc.ReadPickleFile(filePathNm)

        if not currData.get('data'):
            currData['data'] = {}   
        currData['columns'] = columns


        for idx in range(len(resData)):
            shcode = resData[idx][0]

            if not currData['data'].get(shcode):
                currData['data'][shcode] = {}
            if not currData['data'][shcode].get('info'):
                currData['data'][shcode]['info'] = []
            currData['data'][shcode]['종목명'] = resData[idx][1]

# ['종목코드', '종목명','사업년도','결산월','업종','업종별배당율','주식배당','액면가','기말주식수',
#                '주당배당금','배당성향','총배당금액','시가배당율']            
            currData['data'][shcode]['info'] = dataProc._MergeData(currData['data'][shcode]['info'] , [resData[idx][2:]])

        dataProc.WritePickleFile(filePathNm, currData) 


# def SyncFinancialInfo(sYear, eYear, currentPageSize = 100):
#      filePathNm = conf.kindPath + "/financial_info.pkl"

#      for year in range(sYear, eYear+1):
#          for fiscalgubun in (['1_4', 'half', '3_4', 'accntclosing', 'conn']):
#             resData, columns = kind.GetFinancialInfo(year, fiscalgubun, currentPageSize)

#### 데이터 구조 고민 필요