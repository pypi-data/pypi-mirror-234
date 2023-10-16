from   bs4      import BeautifulSoup as bs
import time  
import pandas   as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

import datetime

# here = os.path.dirname(__file__)
# sys.path.append(os.path.join(here, '..'))
# import common.urlProc as urlProc
from ..common  import urlProc
    
#######################################################################3    

# Url에서 특정 조회조건의 값을 추출
GetUrlAttrValue = lambda url, key: [x for x in url.split('&') if x[0:len(key)] == key][0].split('=')[1]

def GetBalticIndex(sDate, eDate):
    resData = []
    # 최초 url
    url = "https://www.shippingnewsnet.com/sdata/page.html?term=Search&sDate={}-{}-{}&eDate={}-{}-{}"
    url = url.format(sDate[0:4], sDate[4:6], sDate[6:8], eDate[0:4], eDate[4:6], eDate[6:8])
      
    # res = req.get(url)
    res = urlProc.requests_url_call(url)

    soup = bs(res.text, "html.parser")

    # 전체 데이터 건수 추출 및 url 조건 추가
    firstPgUrl = soup.select_one("ul.pagination > li.pagination-start > a").get('href')
    url = url  + '&total=%s'%( GetUrlAttrValue(firstPgUrl, 'total')) + '&page={}'
    pgNum = 1
    
    while True:    
        time.sleep(0.1)
        for tr in soup.select("table.marbtm-20 > tbody > tr"):
            tds = tr.select("td")
            resData.append([td.string if '-' in td.string else int(td.string.replace(',',''))  for td in tds])

        pgNum += 1

        if  soup.select_one("ul.pagination > li.pagination-next") or \
            str(pgNum) in [x.get_text() for x in soup.select("ul.pagination > li > a")]:    
            
            # res = req.get(url.format(pgNum))
            res = urlProc.requests_url_call(url.format(pgNum))
            soup = bs(res.text, "html.parser")
        else:
            break
    
    resData.sort()
    
    return pd.DataFrame(resData, columns=['일자', 'BDI','BCI','BPI','BSI'])


#######################################################################
# Naver 크롤링
#######################################################################    
# HName : [ EngCode, 카테고리, 소수점자리수, PC/모바일, BS(뷰티풀숲)/SL(selenium), Remark, Symbol] 
indexList = {
    '유로' :         ['FX_EURKRW', '환율',     2, 'PC', 'BS', '유로화환율', 'EURO' ],
    '달러' :         ['FX_USDKRW', '환율',     1, 'PC', 'BS', '달러화환율', 'USD' ],
    '엔' :           ['FX_JPYKRW', '환율',     2, 'PC', 'BS', '엔화환율', 'JPY'],
    '위안' :         ['FX_CNYKRW', '환율',     2, 'PC', 'BS', '위안화환율', 'CNY'],
    '휘발유' :       ['OIL_GSL',   '유가',     2, 'PC', 'BS', '원/리터'],  
    '고급휘발유' :   ['OIL_HGSL',  '유가',     2, 'PC', 'BS', '원/리터'],  
    '경유' :         ['OIL_LO',    '유가',     2, 'PC', 'BS', '원/리터'],  
    '두바이유' :     ['OIL_DU',    '국제시장', 2, 'PC', 'BS', '달러/배럴'], 
    '브렌트유' :     ['OIL_BRT',   '국제시장', 2, 'PC', 'BS', '달러/배럴'], 
    '텍사스유' :     ['OIL_CL',    '국제시장', 2, 'PC', 'BS', '달러/배럴', 'WTI'], 
    '국제금' :       ['CMDT_GC',   '국제시장', 1, 'PC', 'BS', '달러/트라이온스'], 
    '백금' :         ['CMDT_PL',   '국제시장', 1, 'PC', 'BS', '달러/트라이온스'], 
    '은' :           ['CMDT_SI',   '국제시장', 2, 'PC', 'BS', '달러/트라이온스'], 
    '팔라듐' :       ['CMDT_PA',   '국제시장', 1, 'PC', 'BS', '달러/트라이온스'], 

    '난방유' :       ['CMDT_HO',   '국제시장', 2, 'PC', 'BS', '달러/갤런'], 
    '천연가스' :     ['CMDT_NG',   '국제시장', 2, 'PC', 'BS', '달러/MMBtu'], 
    '구리' :         ['CMDT_CDY',  '국제시장', 1, 'PC', 'BS', '달러/톤'], 
    '납' :           ['CMDT_PDY',  '국제시장', 1, 'PC', 'BS', '달러/톤'], 
    '아연' :         ['CMDT_ZDY',  '국제시장', 1, 'PC', 'BS', '달러/톤'], 
    '니켈' :         ['CMDT_NDY',  '국제시장', 1, 'PC', 'BS', '달러/톤'], 
    '알루미늄합금' : ['CMDT_AAY',  '국제시장', 1, 'PC', 'BS', '달러/톤'], 
    '주석' :         ['CMDT_SDY',  '국제시장', 1, 'PC', 'BS', '달러/톤'], 
    '옥수수' :       ['CMDT_C',    '국제시장', 2, 'PC', 'BS', '센트/부셸'], 
    '설탕' :         ['CMDT_SB',   '국제시장', 2, 'PC', 'BS', '센트/파운드'], 
    '대두' :         ['CMDT_S',    '국제시장', 2, 'PC', 'BS', '센트/부셸'], 
    '대두박' :       ['CMDT_SM',   '국제시장', 2, 'PC', 'BS', '달러/숏톤'], 
    '대두유' :       ['CMDT_BO',   '국제시장', 2, 'PC', 'BS', '센트/파운드'], 
    '면화' :         ['CMDT_CT',   '국제시장', 2, 'PC', 'BS', '센트/파운드'], 
    '소맥' :         ['CMDT_W',    '국제시장', 2, 'PC', 'BS', '센트/부셸'], 
    '쌀' :           ['CMDT_W',    '국제시장', 2, 'PC', 'BS', '달러/cwt'], 
            
    '미니크루드오일':['QMcv1',     '에너지',   2, '모바일', 'SL', '달러/배럴'], 
    '미니난방유' :   ['QHc1',      '에너지',   2, '모바일', 'SL', '달러/갤런'], 
    '가스오일' :     ['LGOcv1',    '에너지',   2, '모바일', 'SL', '달러/톤'], 
    '미니천연가스' : ['QGcv1',     '에너지',   2, '모바일', 'SL', '달러/MMBtu'],        
    '철광석' :       ['TIOc1',     '금속',     2, '모바일', 'SL', '달러/DMT'], 
    '현미'  :        ['RRcv1',     '농산물',   2, '모바일', 'SL', '센트/CWT'],           
    '오렌지주스' :   ['OJcv1',     '농산물',   2, '모바일', 'SL', '센트/파운드'],         
    '커피' :         ['KCcv1',     '농산물',   2, '모바일', 'SL', '센트/파운드'],
    '코코아' :       ['CCcv1',     '농산물',   2, '모바일', 'SL', '달러/톤'], 
    '생우' :         ['LCcv1',     '농산물',   2, '모바일', 'SL', '센트/파운드'],         
    '비육우' :       ['FCcv1',     '농산물',   2, '모바일', 'SL', '센트/파운드'],   
    
}

urlDict = {
    'PC' : {
            'BaseURL'  : "https://finance.naver.com/marketindex",
            '환율'     : "/exchangeDailyQuote.naver?marketindexCd={}&page={}",
            '유가'     : "/oilDailyQuote.naver?marketindexCd={}&page={}",
            '국제시장' : "/worldDailyQuote.naver?fdtc=2&marketindexCd={}&page={}",
    },
    '모바일' : {
            'BaseURL'  : "https://m.stock.naver.com/marketindex",
            '농산물'   : "/agricultural/{}",
            '에너지'   : "/energy/{}",
            '금속'     : "/metals/{}",
    },
    
}


def GetNaverMarketIndex(mIndexNm, sDate, eDate):
    resData = []
    mIndexCd = indexList[mIndexNm][0]
    category = indexList[mIndexNm][1]
    float_digits = indexList[mIndexNm][2] # 소수점 이하 숫자갯수
    deviceType = indexList[mIndexNm][3]  # PC / 모바일
    crawlingType = indexList[mIndexNm][4]  # BeautifulSoup / Selenium
    
    # 최초 url
    url = urlDict[deviceType]["BaseURL"] + urlDict[deviceType][category]    
    pgNum = 1                
    
    ## BeautifulSoup 처리
    if crawlingType == 'BS':
        res = urlProc.requests_url_call(url.format(mIndexCd, pgNum))

        soup = bs(res.text, "html.parser")

        # 전체 데이터 건수 추출 및 url 조건 추가
        jobInd = True
        while jobInd:    
            time.sleep(0.1)
            trs = soup.select("body > div > table > tbody > tr")
            for tr in trs:
                tds = tr.select("td")

                curDt = tds[0].get_text().strip().replace('.','')
                if sDate <= curDt and curDt <= eDate:
                    resData.append([ curDt,
                                     round(float(tds[1].get_text().strip().replace(',','')), float_digits) ] )
                elif curDt < sDate:
                    jobInd = False                    
            
            if  jobInd and (len(trs) > 0):    
                pgNum += 1
                res = urlProc.requests_url_call(url.format(mIndexCd, pgNum))
                soup = bs(res.text, "html.parser")
            else:
                break
                
    ## Selenium 처리 - start
    elif crawlingType == 'SL':
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("window-size=1000,1000")
        options.add_argument("no-sandbox") ## 탭간에 옮겨 다니면서 원하는 액션 수행 가능

        s=Service("./chromedriver.exe")
        chrome = webdriver.Chrome(service=s, options=options)
        wait = WebDriverWait(chrome, 10)
        short_wait = WebDriverWait(chrome, 3)        
        
        # 데이터 조회 (Selenium)
        d_today = datetime.date.today()
        s_YYYY = d_today.year
        s_MMDD = d_today.strftime('%m%d')        
        
        url = url.format(mIndexCd)
        
        print(url)        
        chrome.get(url) 
        
        while True:
            dataList = chrome.find_elements(By.XPATH, "//tbody/tr[@class]")
            
            # 조회기간 시작일자에 도달하였거나, 조회 데이터가 없는 경우 stop
            if len(dataList) > 0:
                last_MMDD = dataList[-1].find_elements(By.TAG_NAME, "td")[0].text.replace('.','')
                if s_MMDD < last_MMDD: # 년도가 바뀐 경우
                    s_YYYY -= 1
                s_MMDD = last_MMDD
                
                print('\r', datetime.datetime.now(), str(pgNum) + '페이지 처리 완료 :', str(s_YYYY)+s_MMDD, end='')
                if (str(s_YYYY) + s_MMDD) <= sDate:
                    break
            else: 
                break
            
            # 다음 조회 버튼이 있는 경우 다음 버튼 click 처리
            if chrome.find_elements(By.CLASS_NAME, "InfinityMoreButton_button__ETrlQ"):
                chrome.find_elements(By.CLASS_NAME, "InfinityMoreButton_button__ETrlQ")[0].click()
                time.sleep(1)
            else:
                break
            
            pgNum += 1                

        #-------------#
        # 데이터 추출 #
        #-------------#
        s_YYYY = d_today.year
        s_MMDD = d_today.strftime('%m%d')   

        itmeList = chrome.find_elements(By.XPATH, "//tbody/tr[@class]")
        if len(itmeList):
            for data in itmeList:

                # 날짜 처리
                c_MMDD = data.find_elements(By.TAG_NAME, "td")[0].text.replace('.','')
                if s_MMDD < c_MMDD: # 년도가 바뀐 경우
                    s_YYYY -= 1
                s_MMDD = c_MMDD        
                curDt = str(s_YYYY) + c_MMDD

                if sDate <= curDt and curDt <= eDate:
                    val = data.find_elements(By.TAG_NAME, "td")[1].text
                    resData.append([ curDt,
                                     round(float(val.replace(',','')), float_digits) ] )                
        chrome.close()
    ## Selenium 처리 - end
        
    resData.sort()
        
    return pd.DataFrame(resData, columns=['일자', mIndexNm])

