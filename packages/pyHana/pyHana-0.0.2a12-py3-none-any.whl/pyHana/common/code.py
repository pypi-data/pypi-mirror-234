from . import conf, dataProc
import pandas as pd


# 증권사에서 조회한 데이터를 파일로 저장하여, 데이터 분석 시 사용 (분석 수행 시 증권사 IF 최소화)
# 화면별 저장할 컬럼 정의
saveColumns = {
    "일별주가" : ['일자', '시가', '고가', '저가', '종가', '거래량', '거래대금'],
    "t3518"    : ['일자', '종가'],
}


# 금감원과 이베스트 증권에서 관리하는 회사명이 다름

# 금감원 자료 처리시에 사용
# def _GetShcodeDart(title):    
#     filePathNm = conf.companyInfoPath + "/기업list(금감원).pkl"    
#     stockItemList = dataProc.ReadPickleFile(filePathNm)    
               
#     if stockItemList['회사명'].get(title):
#         retVal = [ stockItemList['회사명'][title], title ]
#     else:
#         retVal = []
        
#     return retVal

# def _GetCmpnyNameDart(shCode):    
#     filePathNm = conf.companyInfoPath + "/기업list(금감원).pkl"    
#     stockItemList = dataProc.ReadPickleFile(filePathNm)    
    
#     if stockItemList['종목코드'].get(shCode):
#         retVal = [ shCode, stockItemList['종목코드'][shCode]  ]
#     else:
#         retVal = []
               
#     return retVal

# def _GetStockItemListDart(srchItem):
#     itemList = _GetCmpnyNameDart(srchItem)
#     if len(itemList) == 0:
#         itemList = _GetShcodeDart(srchItem) 
    
#     return itemList
def _GetStockItemListDart(srchItem):
    filePathNm = conf.companyInfoPath + "/기업list(금감원).pkl"    
    df = dataProc.ReadPickleFile(filePathNm)    

    dfRes = df[df['회사명']==srchItem]
    if len(dfRes) == 0:
        dfRes = df[df['종목코드']==srchItem]
    
    return dfRes

def _GetStockItemListDartAll(srchItem): 
    filePathNm = conf.companyInfoPath + "/기업list(금감원).pkl"    
    df = dataProc.ReadPickleFile(filePathNm)    

    dfRes = df[df['회사명'].str.contains(srchItem)]
    if len(dfRes) == 0:
        dfRes = df[df['종목코드'].str.contains(srchItem)]
    
    return dfRes


# 회사명, 종목코드 추출 시 기본적으로 ebest 데이터 사용
# def _GetShcode(title):    
#     filePathNm = conf.stockInfoPath + "/stockitem_list.pkl"    
#     df = dataProc.ReadPickleFile(filePathNm)    

#     return df[df['종목명']==title]

def _GetCmpnyName(shCode):    
    df = dataProc.ReadPickleFile( conf.stockInfoPath + "/stockitem_list.pkl" )    

    return df[df['종목코드']==shCode]

def GetStockItem(srchItem):
    df = dataProc.ReadPickleFile( conf.stockInfoPath + "/stockitem_list.pkl" )    

    dfRes = df[df['종목명']==srchItem] 
    if len(dfRes) == 0:
        dfRes = df[df['종목코드']==srchItem]
    
    return dfRes

def GetStockItemListAll(title=''):   
    """
    종목명 return
    """
    filePathNm = conf.stockInfoPath + "/stockitem_list.pkl"
    df = dataProc.ReadPickleFile(filePathNm)

    return df[df['종목명'].str.contains(title)]