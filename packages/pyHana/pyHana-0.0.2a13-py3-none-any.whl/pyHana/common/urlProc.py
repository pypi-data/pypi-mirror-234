import requests
import time
# import datetime as dt

def requests_url_call(urlStr):
    errInd = 'N'
    
    print('\r' + urlStr, end='')

    while(1):
        try:                             
            resp = requests.get(urlStr, timeout=(5, 60)) # connect timeout 5초, read timeout 30로 각각 설정             
            if errInd == 'Y':
                print('>> Requests retry success : ', flush=True)              
            return resp
        
        except Exception as e:
            print("\n", ':', type(e), ':',  e, flush=True)
            errInd = 'Y'
            time.sleep(5)

    print('\r', end='')            
    return resp