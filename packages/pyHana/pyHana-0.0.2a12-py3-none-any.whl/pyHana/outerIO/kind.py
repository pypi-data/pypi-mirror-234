from   bs4      import BeautifulSoup as bs
import time  
import re
import pandas   as pd
from ..common   import urlProc
import json    

# Url에서 특정 조회조건의 값을 추출
# GetUrlAttrValue = lambda url, key: [x for x in url.split('&') if x[0:len(key)] == key][0].split('=')[1]

def GetStockTradeInfo(srchDt):
    urlTmp = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd?bld=dbms/MDC/STAT/standard/MDCSTAT01501&locale=ko_KR&mktId=ALL&share=1&money=1&csvxls_isNo=false&trdDd={}"
        
    url = urlTmp.format(srchDt)
    res = urlProc.requests_url_call(url)    
    dList = json.loads(res.text)['OutBlock_1']

    rData = []
    errCnt = 0

    for data in dList:
        if data['TDD_OPNPRC'] != '-':
            rData.append([ data['ISU_SRT_CD'], data['ISU_ABBRV'], srchDt, 
                        data['TDD_OPNPRC'].replace(",",""), data['TDD_HGPRC'].replace(",",""), 
                        data['TDD_LWPRC'].replace(",",""), data['TDD_CLSPRC'].replace(",",""), 
                        data['ACC_TRDVOL'].replace(",",""), 
                        str(int(int(data['ACC_TRDVAL'].replace(",",""))/1000000))
                        ])
        else:
            errCnt += 1
    
    if errCnt > 0:
        print("\n", srchDt, "전체대상 : ", len(dList), " , SKIP건수 : ", errCnt)
        
    return pd.DataFrame( rData, columns=['종목코드', '종목명', '일자', '시가', '고가', '저가', '종가', '거래량', '거래대금'] )


def GetDividendInfo(selYear, currentPageSize = 100, marketType='', settlementMonth='', yearCnt = 3):
    # currentPageSize(페이지당 조회건수) : 15 / 30 / 50 / 100
    # marketType(시장구분) : 전체 '', 유가증권 '1', 코스닥 '2' 코넥스 '6' 
    # settlementMonth(결산월) : 전체 '', 1월~12월 : '01'~'12'
    # selYearCnt(최근 몇년간 조회) : 1 / 2 / 3 
    # selYear : 기준년도 (해당 년도를 기준으로 최근 이전 {selYearCnt} 년간 자료 조회)

    columns = ['종목코드','종목명','사업년도','결산월','업종','업종별배당율','주식배당','액면가','기말주식수',
               '주당배당금','배당성향','총배당금액','시가배당율']

    resData = []

    urlTmp = "https://kind.krx.co.kr/disclosureinfo/dividendinfo.do?method=searchDividendInfoSub&forward=dividendinfo_sub"
    urlTmp += "&searchCodeType=&searchCorpName=&repIsuSrtCd=&chkOrgData=&searchCorpNameTmp="
    urlTmp += "&currentPageSize={}&marketType={}&settlementMonth={}".format(currentPageSize, marketType, settlementMonth)
    urlTmp += "&selYear={}&selYearCnt={}&pageIndex={}"    

    pgNum = 1
    while True:                
        # res = req.get(url)
        url = urlTmp.format(selYear, yearCnt, pgNum)
        res = urlProc.requests_url_call(url)

        soup = bs(res.text, "html.parser")

        trs = soup.tbody.select("tr")
        for tr in trs:    
            tds = tr.select("td")
            tdCnt = len(tds)
            
            for idx, td in enumerate(tds):
                if idx == 0:
                    if tdCnt == 12: 
                        shcode = td.select_one("a#companysum").get("onclick").split("'")[1]
                        if len(shcode) == 5:
                            shcode += '0'
                        title = td.get("title")
                    trVal = [shcode, title]
                
                if not (idx ==0 and tdCnt == 12):
                    val = td.text.strip().replace(",","").replace("-","0")
                    if (idx - tdCnt + 11) in (3,4,7,8,10):
                        val = float(re.sub(r"[^0-9.,]", "", val))
                    elif (idx - tdCnt + 11) in (5,6,9):
                        val = int(re.sub(r"[^0-9.,]", "", val))
                    trVal.append(val)
                    
            resData.append(trVal)

        x=soup.select_one("section.paging-group div.info strong")
        curNum = int(x.text)
        totNum = int(x.next_sibling.split("/")[1].split("\xa0")[0])

        if curNum >= totNum:
            break

        pgNum += 1
        
        time.sleep(0.1)
    
    return pd.DataFrame(resData, columns=columns)

# def GetFinancialInfo(year, fiscalgubun, currentPageSize = 100):
#     columns = ['종목코드','종목명','유동자산','고정자산','자산총계','유동부채','고정부채','부채총계','자본금',
#                '자본잉여금','이익잉여금','자본총계','매출액','영업이익','세전이익','당기순이익']
    
#     resData = []

#     urlTmp = "https://kind.krx.co.kr/compfinance/financialinfo.do?method=searchFinancialInfoWithRange&forward=list"
#     urlTmp += "&finsearchtype=finstat&titleofaccnt=A010%7CA040%7CA080%7CA090%7CA100%7CA110%7CA120%7CA130%7CA140%7CA160%7CA170%7CA180%7CA190%7CA200"
#                                                 # A010|A040|A080|A090|A100|A110|A120|A130|A140|A160|A170|A180|A190|A200
#     # urlTmp += "&orderMode=A080&orderStat=D"  # 자산총계 역순 정렬 (생략)    
#     urlTmp += "&fromDate=&toDate="
#     urlTmp += "&A010=checkbox&a010_from=&a010_to=" # 유동자산
#     urlTmp += "&A040=checkbox&a040_from=&a040_to=" # 고정자산
#     urlTmp += "&A080=checkbox&a080_from=&a080_to=" # 자산총계
#     urlTmp += "&A090=checkbox&a090_from=&a090_to=" # 유동부채
#     urlTmp += "&A100=checkbox&a100_from=&a100_to=" # 고정부채
#     urlTmp += "&A110=checkbox&a110_from=&a110_to=" # 부채총계
#     urlTmp += "&A120=checkbox&a120_from=&a120_to=" # 자본금
#     urlTmp += "&A130=checkbox&a130_from=&a130_to=" # 자본잉여금
#     urlTmp += "&A140=checkbox&a140_from=&a140_to=" # 이익잉여금
#     urlTmp += "&A160=checkbox&a160_from=&a160_to=" # 자본총계
#     urlTmp += "&A170=checkbox&a170_from=&a170_to=" # 매출액
#     urlTmp += "&A180=checkbox&a180_from=&a180_to=" # 영업이익
#     urlTmp += "&A190=checkbox&a190_from=&a190_to=" # 세전이익
#     urlTmp += "&A200=checkbox&a200_from=&a200_to=" # 당기순이익
#     urlTmp += "&acntgType=I&isfirst=false&marketType=all&industry="
#     urlTmp += "&currentPageSize={}&fiscalyear={}&fiscalgubun={}".format(currentPageSize, year, fiscalgubun)
#     urlTmp += "&pageIndex={}"


#     pgNum = 1
#     while True:                
#         # res = req.get(url)
#         url = urlTmp.format(pgNum)
#         res = urlProc.requests_url_call(url)

#         soup = bs(res.text, "html.parser")

#         trs = soup.tbody.select("tr")
#         for tr in trs:    
#             tds = tr.select("td")

#             for idx, td in enumerate(tds):
#                 if idx == 1:
#                     shcode = td.select_one("a#companysum").get("onclick").split("'")[1]
#                     if len(shcode) == 5:
#                         shcode += '0'
#                     title = td.select_one("a#companysum").get("title")
                    
#                     trVal = [shcode, title]
                    
#                 elif idx > 1:        
                    
#                     val = re.sub(r"[^0-9]", "", td.text.strip())
                    
#                     if len(val) > 0:
#                         val = int(val)
#                     else:
#                         val = 0
                                
#                     trVal.append(val)

#             resData.append(trVal)

#         x=soup.select_one("section.paging-group div.info strong")
#         curNum = int(x.text)
#         totNum = int(x.next_sibling.split("/")[1].split("\xa0")[0])
        
#         if curNum >= totNum:
#             break

#         pgNum += 1

#         time.sleep(0.1)
    
#     return resData, columns