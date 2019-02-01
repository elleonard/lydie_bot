import discord
import yaml
import json
import os
import sys
import re
import random
from datetime import datetime

import gspread

import config
import commands

client = discord.Client()

@client.event
async def on_ready():
  print('こんにちはー！')

@client.event
async def on_message(message):
  if client.user.id in message.content:
    if commands.EVENT_SCHEDULE.text in message.content:
      await client.send_message(message.channel, get_game_events_text())
    if commands.ORUGA_ITSUKA.text in message.content:
      await client.send_message(message.channel, "止まるんじゃねえぞ ってスーちゃんが言ってたけどなんのこと？")
    if commands.FGO_EVENT.text in message.content:
      await client.send_message(message.channel, "konさんに聞いたほうが早いと思うよ https://twitter.com/niconikon01")
    if commands.SPREADSHEET.text in message.content:
      await client.send_message(message.channel, "ここだよ\n"+get_spreadsheet_urls())
    if commands.BARREL.text in message.content:
      await client.send_message(message.channel, get_barrel())
    if commands.HELP.text in message.content:
      await client.send_message(message.channel, get_help_text())

def get_barrel():
  rand = random.randint(0,2)
  if rand == 0:
    return 'たるですよ'
  if rand == 1:
    return 'たるだけに最近たるんで……な、なんでもない！'
  return 'たーる'

def get_game_events():
  credentials = config.get_google_credentials()
  gsc = gspread.authorize(credentials)
  sheet = gsc.open('ソシャゲイベント一覧').sheet1
  return sheet.get_all_records(False, 1)

def time_left(to):
  now = datetime.now()
  if re.match(r"\d{4}-\d{2}-\d{2} \d{1,2}:\d{2}", to):
    to_datetime = datetime.strptime(to, '%Y-%m-%d %H:%M')
    return to_datetime - now
  if re.match(r"\d{4}-\d{2}-\d{2}", to):
    to_datetime = datetime.strptime(to, '%Y-%m-%d')
    return to_datetime - now
  return None

def timedelta_text(delta):
  """timedeltaから表示用のテキストを生成します
  
  Args:
    delta (timedelta): 生成に用いるtimedelta
  
  Returns:
    str: 表示用テキスト
  """
  if delta.days > 0:
    return "あと**"+str(delta.days)+"日**"
  if delta.seconds > 3600:
    return "あと**"+str(int(delta.seconds/3600))+"時間**"
  if delta.seconds > 60:
    return "あと**"+str(int(delta.seconds/60))+"分**"
  return "終了済み"

def get_game_events_text():
  event_list = get_game_events()
  text = ""
  for event_data in event_list:
    text += event_data['ソシャゲ名'] + " の " + event_data['イベント名'] + " は " + event_data['イベント終了'] + " まで"
    delta = time_left(event_data['イベント終了'])
    if delta is not None:
      text += "（" + timedelta_text(delta) + "）"
    text += "\n"
  return text + "だよ"

def get_help_text():
  help_text = "コマンド一覧\n"
  for command in commands.list:
    help_text += command.text+": "+command.help+"\n"
  return help_text

def get_spreadsheet_urls():
  return "イベントいつまで: " + os.environ["SPREADSHEET_EVENT"]

client.run(os.environ["DISCORD_ACCESS_TOKEN"])
