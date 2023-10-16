from   bs4      import BeautifulSoup as bs
import time  
import re
import pandas  as pd
from ..common  import urlProc

def GetCmpnyAcntInfo(year, quarter, selectToc=5, currentPageSize = 100):
    # selectToc : 0 (연결재무제표), 5(재무제표)
    # reportCode : 11013(1분기), 11012(반기), 11014(3분기), 11011(사업보고서)
    if   quarter == 1:  reportCode = ['11013','1분기']
    elif quarter == 2:  reportCode = ['11012','반기']
    elif quarter == 3:  reportCode = ['11014','3분기']
    elif quarter == 4:  reportCode = ['11011','사업']
    else:               reportCode = ['','']    

    # columns = ['자산총계','부채총계','자본총계','유동자산','유동부채','자본금','비유동자산','비유동부채','이익잉여금',
    #            '매출액','당기순이익','영업이익','세전이익']
    columns = ['유동자산','비유동자산','자산총계','유동부채','비유동부채','부채총계','자본금','이익잉여금','자본총계',
               '매출액','영업이익','세전이익','당기순이익']
    
    resData = []

    urlTmp = "https://opendart.fss.or.kr/disclosureinfo/fnltt/cmpnyacnt/list.do?sortStdr=&sortOrdr=asc"
    urlTmp += "&textCrpCik=&textCrpNm=&typesOfBusiness=&corporationType=&accountGubunAll=on"
    urlTmp += "&accountGubun=1" # 유동자산
    urlTmp += "&accountGubun=2" # 비유동자산
    urlTmp += "&accountGubun=3" # 자산총계
    urlTmp += "&accountGubun=4" # 유동부채
    urlTmp += "&accountGubun=5" # 비유동부채
    urlTmp += "&accountGubun=6" # 부채총계
    urlTmp += "&accountGubun=7" # 자본금
    urlTmp += "&accountGubun=8" # 이익잉여금
    urlTmp += "&accountGubun=9" # 자본총계
    urlTmp += "&accountGubun=10" # 매출액
    urlTmp += "&accountGubun=11" # 영업이익
    urlTmp += "&accountGubun=12" # 법인세차감전순이익
    urlTmp += "&accountGubun=13" # 당기순이익  
    urlTmp += "&recordCountPerPage={}&selectYear={}&reportCode={}&selectToc={}".format(currentPageSize, year, reportCode[0], selectToc)
    urlTmp += "&pageIndex={}"
               
    skipCnt = 0
    pgNum = 1
    while True:                
        # res = req.get(url)
        url = urlTmp.format(pgNum)

        res = urlProc.requests_url_call(url)

        soup = bs(res.text, "html.parser")

        trs = soup.tbody.select("tr")
        for tr in trs:    
            tds = tr.select("td")

            tdVal = []
            for idx, td in enumerate(tds):
                if idx == 0:
                    
                    title = td.select_one("span.com").text
                    fiscalMon = td.p.text.strip() 
                    
                    if fiscalMon == '(-)':
                        # print('skip >> ', title)
                        skipCnt += 1
                        break
                    
                    fiscalMon = fiscalMon.split(",")[1].replace("결산)","")
                    if fiscalMon == '03월':
                        quarterNew = (quarter + 1) if quarter <=3 else 1
                    else:
                        quarterNew = quarter
                    # 종목명, 결산월, 기준년도, 기준분기, 보고서종류
                    tdVal = [title, fiscalMon, year, quarterNew, reportCode[1]]
                else:        
                    val = re.sub(r"[^0-9]", "", td.text.strip())
                    if len(val) > 0:
                        val = int(val)
                    tdVal.append(val)

            if len(tdVal) > 0:
                resData.append(tdVal)        

        x=soup.select_one("div.page_info").text.replace(",","")
        curNum = int(x.split("/")[0][1:])
        totNum = int(x.split("/")[1].split("]")[0])
        
        if curNum >= totNum:
            break

        pgNum += 1

        time.sleep(0.1)
    
    totRecCnt = soup.select_one("div.page_info").text.replace(" ","").split("총")[1].replace("건]","")
    print('\r', year, reportCode[1], selectToc, ' >> 대상:', totRecCnt, '제외:', skipCnt, '', len(resData), ' '*40)

    # return resData, ['종목명', '결산월', '기준년도', '기준분기', '보고서종류'] + columns
    return pd.DataFrame(resData, columns = ['종목명', '결산월', '기준년도', '기준분기', '보고서종류'] + columns)


def GetCmpnyList():
    columns = ['회사명','종목코드']
    
    resData = []

    urlTmp = "https://dart.fss.or.kr/dsae001/search.ax?startDate=&endDate=&maxResults=&maxLinks=&autoSearch=true&businessCode=all"
    urlTmp += "&sort=&series=&selectKey=&searchIndex=&textCrpCik=&bsnRgsNo=&bsnRgsNo_1=&bsnRgsNo_2=&bsnRgsNo_3=&crpRgsNo=&textCrpNm="
    urlTmp += "&corporationType={}&currentPage={}"

    for corpType in ('P','A'):
        pgNum = 1
        while True:                
            url = urlTmp.format(corpType, pgNum)

            res = urlProc.requests_url_call(url)

            soup = bs(res.text, "html.parser")

            trs = soup.tbody.select("tr")
            
            for tr in trs:    
                title = tr.td.a.text.strip()
                shCode = tr.td.next_sibling.next_sibling.text
                
                resData.append([title, shCode])

            x=soup.select_one("div.pageInfo").text.replace(",","")
            curNum = int(x.split("/")[0][1:])
            totNum = int(x.split("/")[1].split("]")[0])

            if curNum >= totNum:
                break

            pgNum += 1

            time.sleep(0.1)

        totRecCnt = soup.select_one("div.pageInfo").text.replace(" ","").split("총")[1].replace("건]","")
        print('\ncorporationType(', corpType, ') : ', totRecCnt, '건 추출')

    return pd.DataFrame(resData, columns=columns)