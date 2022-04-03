import csv
import datetime
import pandas as pd
import logging
import re
import os
import sys
import twitter
import tweepy
import keys

def main():
    logging.info("======MAIN METHOD START======")
    dtNow = datetime.datetime.now()
    df = pd.read_csv('../conf/games_sanf.csv')
    for i in df.itertuples():
        subject = str(i.Subject)
        game_id = str(i.Description) + '_' + subject
        location = str(i.Location)
        logging.info('対象: ' + game_id + ' @' + location)
        date_str = str(i[2]) + ' ' + str(i[3])
        msg = '\n' + game_id + ' @' + location + ' ' + date_str + ' KickOff'
        if(not(checkDate(date_str))):
            logging.info('日付形式がおかしい（まだ入ってない）のでスキップ')
        elif(re.search("^TM.*",subject) != None):
            logging.info('TMなのでスキップ')
        else:            
            noticeGameSchedule(msg, game_id, dtNow, datetime.datetime.strptime(date_str,'%Y/%m/%d %H:%M:%S'))
    logging.info("======MAIN METHOD END======")
    
def noticeGameSchedule(msg, game_id, dtNow, game_date):
    logging.info("===METHOD START--noticeGameStarting-- ===")
    diffTime = game_date - dtNow
    raishu="raishu"
    ashita="ashita"
    mosugu="mosugu"
    joban="joban"
    shuban="shuban"
    
    if (diffTime >= datetime.timedelta(hours=7*24)) :
        logging.info('リマインド対象外（まだだいぶ先）')
    elif (diffTime < datetime.timedelta(hours=7*24) and datetime.timedelta(hours=24) <= diffTime) :
        remind_kbn = raishu
        msg = '来週くらいに試合があるで。' + msg
        doNotice(game_id,remind_kbn,msg)
    elif (diffTime < datetime.timedelta(hours=24) and datetime.timedelta(hours=1) <= diffTime):
        remind_kbn = ashita
        msg = '明日くらいに試合があるで。' + msg
        doNotice(game_id,remind_kbn,msg)
    elif (diffTime < datetime.timedelta(minutes=15) and datetime.timedelta(hours=0) <= diffTime):
        remind_kbn = mosugu
        msg = 'もうすぐ試合はじまるで。' + msg
        doNotice(game_id,remind_kbn,msg)
    elif (diffTime < datetime.timedelta(hours=0) and datetime.timedelta(minutes=-30) <= diffTime):
        remind_kbn = joban
        msg = 'もうはじまっとるけどまだ序盤で、応援しようや。' + msg
        doNotice(game_id,remind_kbn,msg)
    elif (diffTime < datetime.timedelta(minutes=-30) and datetime.timedelta(minutes=-80) <= diffTime):
        remind_kbn = shuban
        msg = '多分もう終盤じゃけどまだ間に合うで、応援しようや。' + msg
        doNotice(game_id,remind_kbn,msg)
    elif (diffTime < datetime.timedelta(minutes=-80)):
        logging.info('リマインド対象じゃない（もうおわってる）')
    else :
        logging.info('例外')
   
    logging.info("===METHOD END --noticeGameStarting-- ===")
    logging.info("")
    logging.info("")

def doNotice(game_id, remind_kbn, msg):
    logging.info("===METHOD START --doNotice-- ===")
    if(os.path.exists('../elements/' + game_id + '_' + remind_kbn)):
        # あったらスキップ
        logging.info("フラグファイルあり。投稿済の為スキップします。")
    else:
        # なかったらフラグ作って実施
        with open('../elements/' + game_id + '_' + remind_kbn, 'w' ,encoding='utf-8') as f:
            f.write('')
        #TODO Twitter API 実行
        # 取得したキーとアクセストークンを設定する
        client = tweepy.Client(consumer_key=keys.consumer_key,consumer_secret=keys.consumer_secret,access_token=keys.token,access_token_secret=keys.token_secret)
        # print(auth)
        logging.info("tweetします： " + "\n" + msg + "\n")
        client.create_tweet(text=msg)
        logging.info("tweetしました： " + "\n" + msg + "\n")

    logging.info("===METHOD START --doNotice-- ===")

def checkDate(date_str):
    try:
        newDate=datetime.datetime.strptime(date_str,'%Y/%m/%d %H:%M:%S')
        return True
    except ValueError:
        return False
    
if __name__== "__main__":
    try:
        MYFORMAT = '[%(asctime)s]%(filename)s(%(lineno)d): %(message)s'
        dt_now_log = datetime.datetime.now()

        logging.basicConfig(
            filename='../log/' +
            dt_now_log.strftime('%Y%m%d%H%M%S') + '.log',
            filemode='w',  # Default is 'a'
            format=MYFORMAT,
            encoding='utf-8',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=logging.INFO)
        
        main()

    except KeyboardInterrupt:
        logging.info("Interrupted by Ctrl + C")