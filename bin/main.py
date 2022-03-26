import csv
import datetime
import pandas as pd

def main():
    dtNow = datetime.datetime.now()
    df = pd.read_csv('../conf/shiai.csv')
    for i in df.itertuples():
        print('対象：' + str(i[1]) + ' , ' + str(i[8]))
        # if(i[1]==1):
        #     print("break")
        #     break
        # else:
        noticeGameSchedule(dtNow, datetime.datetime.strptime(i[2]+' '+i[3],'%Y/%m/%d %H:%M:%S'))
    
def noticeGameSchedule(beforeTime, dtNow):
    print("method start --noticeGameStarting-- ")
    diffTime = dtNow - beforeTime
    if (diffTime < datetime.timedelta(hours=7*24) and datetime.timedelta(hours=24) <= diffTime) :
        doNotice('来週くらいに試合があるで。応援しようや。')
    elif (diffTime < datetime.timedelta(hours=24) and datetime.timedelta(hours=1) <= diffTime):
        doNotice('明日くらいに試合があるで。応援しようや。')
    elif (diffTime < datetime.timedelta(minutes=15) and datetime.timedelta(hours=0) <= diffTime):
        doNotice('もうすぐ試合はじまるで。応援しようや。')
    elif (diffTime < datetime.timedelta(hours=0) and datetime.timedelta(minutes=-30) <= diffTime):
        doNotice('30分くらい過ぎとるけどまだ間に合うで応援しようや。')
    elif (diffTime < datetime.timedelta(minutes=-30) and datetime.timedelta(minutes=-80) <= diffTime):
        doNotice('多分もう終盤じゃけどまだ間に合うで応援しようや。')
    elif (diffTime < datetime.timedelta(minutes=-80)):
        setOwataF()
    else :
        print('リマインド対象じゃない')
   
    print("method end --noticeGameStarting-- ")
    print("")
    print("")

def doNotice(str):
    print("method start --doNotice-- ")
    print(str)
    print("method end --doNotice-- ")

def setOwataF():
    #OwataFを1に上書く。
    print("method start --setOwataFlag-- ")
    print("method end --setOwataFlag-- ")
    
if __name__== "__main__":
    main()