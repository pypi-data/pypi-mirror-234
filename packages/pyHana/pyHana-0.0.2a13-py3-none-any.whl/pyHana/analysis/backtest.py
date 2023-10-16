import pandas    as pd
import random
from   ..innerIO import stockInfo  as sd

# backtest 수행 : 성능 향상을 위해 dataframe 처리 최소화 버전
def backtest(dfData
           , maxItemNum = 1           # 분산 투자 지수 (각 종목 매수 시 전체 금액의 1/N만큼 투자) 
           , cashAmt = 100000000      # 초기 투자금
           , taxRatio = 0.2           # 거래세(%)
           , expenseRatio = 0.015     # 거래수수료(%) 
           , dayMaxTradeNum = 1       # 일 최대 매수 가능 종목수
           ):  
    invItemList = []  # 투자 진행 종목의 종료일자 - 다음 투자를 위해
    simulRes = []     # 투자 결과 리스트 저장

    # 처리속도 향상을 위해 dataframe -> list 변환 후 수행
    listTradeInfo = dfData[['종목코드','종목명','매수일자','매수가격','매도일자','매도가격']].values.tolist()    
    
    # # input 데이터의 종목수가 분산 투자 주식 수보다 적은 경우 보정처리 => 한 종목으로도 분산 투자 가능하도록 로직 삭제
    # maxItemNum = min(maxItemNum, len(dfData["종목코드"].unique()))
    
    listTradeDt = dfData["매수일자"].unique().tolist()
    listTradeDt.sort()
    
    while(len(listTradeDt) > 0):
        curDt = listTradeDt[0]

        # 투자일 경과 건 투자진행 종목 리스트에서 삭제
        i = 0
        while i < len(invItemList) and invItemList[i] < curDt:
            i += 1
        if i >= 0:
            invItemList = invItemList[i:]

        # maxItemNum 개의 종목에 투자금액 1/N 분배 (이미 투자진행중인 건은 잔존 현금의 투자금액 분배 시 제외)
        ##  cashAmt가 아니라 해당 일자까지 투자한 금액, 회수 못한 금액을 감안한 여유 자금 재계산 필요        
        sellAmtSum = 0
        sellExpenseSum = 0
        for i in range(len(simulRes)):
            # simulRes [종목코드(0),종목명(1),수량(2),매수일자(3),매수가격(4),매수금액(5),매수비용(6),
            #           매도일자(7),매도가격(8),매도금액(9),매도비용(10),손익(11),수익률(%)(12),평가금액(13)                                                  
            if simulRes[i][7] >= curDt:                  # '매도일자'
                sellAmtSum += simulRes[i][9]             # '매도금액'
                sellExpenseSum += simulRes[i][10]        # '매도비용'
        maxInvAmt = (cashAmt - sellAmtSum + sellExpenseSum) / ( maxItemNum - len(invItemList) )

        # 해당 일자에 대한 투자 대상종목 수 계산
        curInvItemNum =  min (maxItemNum - len(invItemList), dayMaxTradeNum )
        # dList = [x for x in listTradeInfo if x[2] == curDt]
        dList = [x for x in listTradeInfo if x[2] == curDt and maxInvAmt >= x[3]] # x[3] 주가. 1주이상 살 수 있는 종목만 list

        if len(dList) > curInvItemNum:
            random.shuffle(dList)
            dList = dList[:curInvItemNum]
        
        for x in dList:
            # 매입일자, 가격 구하기
            buyDt = x[2]
            buyPrice = x[3]
            # 매도일자, 가격 구하기
            sellDt = x[4]      
            sellPrice = x[5]

            #######################################################
            # 매수/매도 거래내역 만들기
            #######################################################
            
            # 주식수량
            buyCnt = int(maxInvAmt / buyPrice)

            # 매입계산
            buyAmt = buyCnt * buyPrice * (-1)
            buyExpense = int(buyAmt * expenseRatio / 100)

            # 매도계산
            sellAmt = buyCnt * sellPrice
            sellExpense = int(sellAmt * taxRatio / 100) * (-1) + int(sellAmt * expenseRatio / 100) * (-1)

            # 보유현금 계산
            deltaAmt = buyAmt + buyExpense + sellAmt + sellExpense
            cashAmt += deltaAmt

            # 거래수익률 계산
            earnRatio = deltaAmt / (buyAmt + buyExpense) * (-100)
             
            # 매도, 매수 결과
            simulRes.append([x[0], x[1], buyCnt, buyDt, buyPrice, buyAmt, buyExpense, 
                             sellDt, sellPrice, sellAmt, sellExpense, deltaAmt, earnRatio, cashAmt] )

            invItemList.append(sellDt)

        invItemList.sort()

        if len(invItemList) >= maxItemNum:
            # 보유 종목 갯수가 max인 경우, 보유종목의 최초 매도일자 이후로 이동
            i = 0
            while( i < len(listTradeDt) ):
                if listTradeDt[i] > invItemList[0]:
                    break
                i += 1

            listTradeDt = listTradeDt[i:]               
        else:
            # 추가 매수 가능한 경우, 다음 시그널 발생일로 이동
            listTradeDt = listTradeDt[1:]      
            
    return pd.DataFrame(simulRes, columns=['종목코드','종목명','수량','매수일자','매수가격','매수금액','매수비용',
                                           '매도일자','매도가격','매도금액','매도비용', '손익','수익률(%)','평가금액'])   

# backtest 수행 : 초기 버전
def backtest_df(dfData
           , maxItemNum = 1           # 분산 투자 지수 (각 종목 매수 시 전체 금액의 1/N만큼 투자) 
           , cashAmt = 100000000      # 초기 투자금
           , taxRatio = 0.2           # 거래세(%)
           , expenseRatio = 0.015     # 거래수수료(%) 
           , dayMaxTradeNum = 1       # 일 최대 매수 가능 종목수
           ):  

    invItemList = []  # 투자 진행 종목의 종료일자 - 다음 투자를 위해
    simulRes = []     # 투자 결과 리스트 저장

    # input 데이터의 종목수가 분산 투자 주식 수보다 적은 경우 보정처리
    maxItemNum = min(maxItemNum, len(dfData["종목코드"].unique()))
    
    dfItemCnt = dfData.groupby("매수일자").agg( 종목수=("종목코드", "count") ).reset_index()    

    while(len(dfItemCnt) > 0):
        curDt = dfItemCnt['매수일자'][0]

        # 투자일 경과 건 투자진행 종목 리스트에서 삭제
        i = 0
        while i < len(invItemList) and invItemList[i] < curDt:
            i += 1
        if i >= 0:
            invItemList = invItemList[i:]

        # maxItemNum 개의 종목에 투자금액 1/N 분배 (이미 투자진행중인 건은 잔존 현금의 투자금액 분배 시 제외)
        ##  cashAmt가 아니라 해당 일자까지 투자한 금액, 회수한 금액을 감안한 여유 자금 재계산 필요
        dfTemp = pd.DataFrame(simulRes, columns=['종목코드','종목명','수량','매수일자','매수가격','매수금액','매수비용',
                                                 '매도일자','매도가격','매도금액','매도비용','현금잔액','투자손익'])    
        dfTemp = dfTemp[dfTemp['매도일자'] >= curDt]

        maxInvAmt = (cashAmt - dfTemp['매도금액'].sum() + dfTemp['매도비용'].sum()) / ( maxItemNum - len(invItemList) )

        # 해당 일자에 대한 투자 대상종목 수 계산
        curInvItemNum =  min (maxItemNum - len(invItemList), dayMaxTradeNum )

    #     print('\n', cashAmt, maxInvAmt, curInvItemNum)

        dList = dfData[dfData['매수일자']==curDt][['종목코드','종목명','매수일자','매수가격',
                                                   '매도일자','매도가격']].values.tolist()
        if len(dList) > curInvItemNum:
            random.shuffle(dList)
            dList = dList[:curInvItemNum]

        for x in dList:
            # 매입일자, 가격 구하기
            buyDt = x[2]
            buyPrice = x[3]
            # 매도일자, 가격 구하기
            sellDt = x[4]      
            sellPrice = x[5]

            #######################################################
            # 매수/매도 거래내역 만들기
            #######################################################
            
            # 주식수량
            buyCnt = int(maxInvAmt / buyPrice)

            # 매입계산
            buyAmt = buyCnt * buyPrice * (-1)
            buyExpense = int(buyAmt * expenseRatio / 100)

            # 매도계산
            sellAmt = buyCnt * sellPrice
            sellExpense = int(sellAmt * taxRatio / 100) * (-1) + int(sellAmt * expenseRatio / 100) * (-1)

            # 보유현금 계산
            deltaAmt = buyAmt + buyExpense + sellAmt + sellExpense
            cashAmt += deltaAmt
    # 
            # 매도, 매수 결과
            simulRes.append([x[0], x[1], buyCnt, buyDt, buyPrice, buyAmt, buyExpense, sellDt, sellPrice, sellAmt, sellExpense, deltaAmt, cashAmt] )

            invItemList.append(sellDt)

        invItemList.sort()

        if len(invItemList) >= maxItemNum:
            # 보유 종목 갯수가 max인 경우, 보유종목의 최초 매도일자 이후로 이동
            dfItemCnt = dfItemCnt[ dfItemCnt['매수일자'] > invItemList[0]            ] [['매수일자','종목수']].reset_index()
        else:
            # 추가 매수 가능한 경우, 다음 시그널 발생일로 이동
            dfItemCnt = dfItemCnt[ dfItemCnt['매수일자'] > dfItemCnt['매수일자'].iloc[0] ] [['매수일자','종목수']].reset_index()

    return pd.DataFrame(simulRes, columns=['종목코드','종목명','수량','매수일자','매수가격','매수금액','매수비용',
                                           '매도일자','매도가격','매도금액','매도비용', '손익','평가금액'])   


# def get_earn_ratio(df, sig_list):
#     i = 0
#     earn_ratio = 100
#     buy_idx = -1
#     sell_idx = -1
                   
#     while(i < len(df)):
#         while( i < len(df) ):
#             if sig_list[i] == 'B':
#                 buy_idx = i
#                 break
#             else:
#                 i += 1

#         while( i < len(df) ):
#             if sig_list[i] == 'S':
#                 sell_idx = i 
#                 earn_ratio *= (df['종가'].iloc[sell_idx] / df['종가'].iloc[buy_idx])

#                 break
#             else:
#                 i += 1
    
#     if buy_idx > sell_idx and buy_idx < (len(df) - 1):
#         sell_idx = len(df) - 1
#         earn_ratio *= (df['종가'].iloc[sell_idx] / df['종가'].iloc[buy_idx])

#     return (earn_ratio - 100)

def backtest_report(  dfStock = []    # backtest 대상 데이터(유효기간)
                    , dfRes   = []    # backtest 결과
                    , pType   = ''):  # 시가/종가
    # # 투자수익률
    invEarnRatio = dfRes.iloc[len(dfRes)-1]['평가금액'] / ( dfRes.iloc[0]['평가금액'] - dfRes.iloc[0]['손익'] ) * 100 - 100

    # # 투자건당 평균 수익률
    # invAvgEarnRatio = sum([ (-1)*x[2]/(x[0]+x[1]) for x in dfRes[['매수금액','매수비용','손익']].values.tolist() ]) * 100 / len(dfRes)
    invAvgEarnRatio = dfRes['수익률(%)'].mean()
    
    # # # 기본 수익률(분석기간)
    basicEarnRatio = ( ( dfStock.iloc[len(dfStock)-1]['종가'] * 0.99785 - dfStock.iloc[0][pType] * 0.00015 )
                     / dfStock.iloc[0][pType] ) * 100 - 100 
    
    # # # 결과 display
    print('투자수익률(backtest) : ', "%7.3f"%( invEarnRatio )+'%', end='   ')
    print('( 거래건수 :', len(dfRes), ', 건당 평균 수익률 :', "%.3f"%(invAvgEarnRatio)+'% )' ) 
    print('기본수익률(분석기간) : ', "%7.3f"%( basicEarnRatio )+'%', end='   ')
    print('( 매수가 :', f"{dfStock.iloc[0][pType]:,}", '[' + dfStock.iloc[0]['일자'] + ']',        
          ', 매도가 :', f"{dfStock.iloc[len(dfStock)-1]['종가']:,}", '[' + dfStock.iloc[len(dfStock)-1]['일자'] + '] )') 

    return invEarnRatio, basicEarnRatio


def get_earn_ratio(dfData):
    earn_ratio = 100
                   
    for i in range(len(dfData)):
        earn_ratio *= (dfData['매도가격'].iloc[i] / dfData['매수가격'].iloc[i])

    return (earn_ratio - 100)