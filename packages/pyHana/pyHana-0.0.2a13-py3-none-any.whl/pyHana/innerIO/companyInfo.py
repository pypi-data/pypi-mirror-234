from ..common import conf, dataProc, code
import pandas as pd


def GetCmpnyFinInfo(srchItem='', unit="억"):
    #acct_list = ['매출액','영업이익','당기순이익','총포괄손익']
    unit_list = {'천' : 1000, '만' : 10000, '백만' : 1000000, '천만' : 10000000, '억' : 100000000, '십억' : 1000000000, '조' : 1000000000000 }
    data = []
    shCodeList = []

    if not unit_list.get(unit):
        print('유효하지 않은 금액단위 > ', unit)
        print('선택가능한 금액단위 > ', unit_list.keys())        
        unit = "억"

    filePathNm = conf.companyInfoPath + "/재무정보(금감원).pkl"
    acntInfo = dataProc.ReadPickleFile(filePathNm)        

    if srchItem == '':
        shCodeList = list(acntInfo['data'].keys())
    else:
        stockItem = code._GetStockItemListDart(srchItem)
        if len(stockItem) == 1:
            shCodeList = [ stockItem.iloc[0]['종목코드'] ]

    shCodeList.sort()
    for shCode in shCodeList:
        data += [ [ shCode, acntInfo['data'][shCode]['종목명'], acntInfo['data'][shCode]['결산월']] +  
                    info[0:3] + [  0 if type(val) == str else int(round(val / unit_list[unit], 0)) for val in info[3:] ]             
                 for info in acntInfo['data'][shCode]['info'] ]

    return pd.DataFrame(data, columns = ['종목코드','종목명','결산월'] + acntInfo['columns'])


def GetDividendInfo(srchItem):
    data = []

    shCode = code.GetStockItem(srchItem).iloc[0][1]
    hName  = code.GetStockItem(srchItem).iloc[0][0]

    filePathNm = conf.companyInfoPath + "/주식배당정보(한국거래소).pkl"
    acntInfo = dataProc.ReadPickleFile(filePathNm)        
    
    if acntInfo['data'].get(shCode) and acntInfo['data'][shCode].get('info'):
        for x in acntInfo['data'][shCode]['info']:
            data.append( [shCode, hName] + x )
    
    return pd.DataFrame(data, columns = ['종목코드','종목명']+acntInfo['columns'])