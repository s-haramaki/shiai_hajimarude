import csv
import datetime
import pandas as pd
import re

def main():
    dtNow = datetime.datetime.now()
    df = pd.read_csv('../conf/games_sanf.csv')
    for i in df.itertuples():
        print('対象：' + str(i[1]) + ' , ' + str(i[8]))
        date_str = str(i[2] + ' ' + str(i[3]))
        subject = str(i[1])
        if(not(checkDate(date_str))):
            print('日付形式がおかしい（まだ入ってない）のでスキップ')
            continue
        elif(re.search("^TM.*",subject) != None):
            print('TMなのでスキップ')
            continue
        else:            
            noticeGameSchedule(dtNow, datetime.datetime.strptime(date_str,'%Y/%m/%d %H:%M:%S'))
    
def noticeGameSchedule(beforeTime, dtNow):
    print("method start --noticeGameStarting-- ")
    diffTime = dtNow - beforeTime
    if (diffTime >= datetime.timedelta(hours=7*24)) :
        doNotice('リマインド対象外（まだだいぶ先）')
    elif (diffTime < datetime.timedelta(hours=7*24) and datetime.timedelta(hours=24) <= diffTime) :
        doNotice('来週くらいに試合があるで。')
    elif (diffTime < datetime.timedelta(hours=24) and datetime.timedelta(hours=1) <= diffTime):
        doNotice('明日くらいに試合があるで。')
    elif (diffTime < datetime.timedelta(minutes=15) and datetime.timedelta(hours=0) <= diffTime):
        doNotice('もうすぐ試合はじまるで。')
    elif (diffTime < datetime.timedelta(hours=0) and datetime.timedelta(minutes=-30) <= diffTime):
        doNotice('30分くらい過ぎとるけどまだ間に合うで、応援しようや。')
    elif (diffTime < datetime.timedelta(minutes=-30) and datetime.timedelta(minutes=-80) <= diffTime):
        doNotice('多分もう終盤じゃけどまだ間に合うで、応援しようや。')
    elif (diffTime < datetime.timedelta(minutes=-80)):
        print('リマインド対象じゃない（もうおわってる）')
    else :
        print('例外')
   
    print("method end --noticeGameStarting-- ")
    print("")
    print("")

def doNotice(str):
    print("method start --doNotice-- ")
    print(str)
    print("method end --doNotice-- ")

def checkDate(date_str):
    try:
        newDate=datetime.datetime.strptime(date_str,'%Y/%m/%d %H:%M:%S')
        return True
    except ValueError:
        return False
    
if __name__== "__main__":
    main()