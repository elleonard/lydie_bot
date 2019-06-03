import gspread
import pytz
import re
from datetime import datetime, timedelta, timezone

import config

JST = timezone(timedelta(hours=+9), 'JST')
jptz = pytz.timezone('Asia/Tokyo')

def get_game_events():
  credentials = config.get_google_credentials()
  gsc = gspread.authorize(credentials)
  sheet = gsc.open('ソシャゲイベント一覧').sheet1
  return sheet.get_all_records(False, 1)

def to_jst_aware(native):
  return jptz.localize(native)

def str_to_datetime(strtime):
  """スプレッドシートから取得した文字列の時刻をdatetime型に変換します。

  Args:
    strtime (str): スプレッドシートから取得した文字列の時刻。
  
  Returns:
    datetime型に変換した時刻。時刻のパースに失敗した場合はNone
  """
  if re.match(r"\d{4}-\d{1,2}-\d{2} \d{1,2}:\d{2}:\d{2}", strtime):
    return to_jst_aware(datetime.strptime(strtime, '%Y-%m-%d %H:%M:%S'))
  if re.match(r"\d{4}-\d{1,2}-\d{2} \d{1,2}:\d{2}", strtime):
    return to_jst_aware(datetime.strptime(strtime, '%Y-%m-%d %H:%M'))
  if re.match(r"\d{4}-\d{1,2}-\d{2}", strtime):
    return to_jst_aware(datetime.strptime(strtime, '%Y-%m-%d'))
  return None

def time_left(to):
  now = datetime.now(JST)
  to_datetime = str_to_datetime(to)
  if to_datetime == None:
    return None
  return to_datetime - now

def timedelta_text(delta):
  """timedeltaから表示用のテキストを生成します
  
  Args:
    delta (timedelta): 生成に用いるtimedelta
  
  Returns:
    str: 表示用テキスト
  """
  if delta.days > 0:
    return "あと**"+str(delta.days)+"日**"
  if delta.days == 0:
    if delta.seconds > 3600:
      return "あと**"+str(int(delta.seconds/3600))+"時間**"
    if delta.seconds > 60:
      return "あと**"+str(int(delta.seconds/60))+"分**"
  # 開始前の場合はこの分岐に入らない
  return "終了済み"

def generate_before_start_text(event_data):
  """イベントが開始前なら、専用のテキストを返します。

  Args:
    event_data (dictionary): スプレッドシートから取得したイベントデータ
  
  Returns:
    str: イベント開始時刻が設定されており、イベント開始前なら専用のテキストを返します。それ以外はNoneを返します。
  """
  if event_data['イベント開始'] == "":
    return None
  start_time = str_to_datetime(event_data['イベント開始'])
  if start_time == None:
    return None
  now = datetime.now(JST)
  delta = start_time - now
  if delta.days < 0:
    return None
  return timedelta_text(delta)


def get_game_events_text():
  event_list = get_game_events()
  text = ""
  for event_data in event_list:
    text += event_data['ソシャゲ名'] + " の " + event_data['イベント名'] + " は "
    before_start_text = generate_before_start_text(event_data)
    if before_start_text == None:
      text += event_data['イベント終了'] + " まで"
      delta = time_left(event_data['イベント終了'])
      if delta is not None:
        text += "（終了まで" + timedelta_text(delta) + "）"
    else:
      text += event_data['イベント開始'] + " から（開始まで" + before_start_text + "）"
    text += "\n"
  return text + "だよ"
