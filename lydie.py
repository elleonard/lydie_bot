import discord
import yaml
import json
import os
import sys

import gspread

from oauth2client.service_account import ServiceAccountCredentials

args = sys.argv

CONFIG_FILE = "./config/config.yml" if len(args) < 2 else args[1]

client = discord.Client()

@client.event
async def on_ready():
  print('こんにちはー！')

@client.event
async def on_message(message):
  if client.user.id in message.content:
    if 'イベントいつまで？' in message.content:
      await client.send_message(message.channel, get_game_events_text(message))
    if '何やってんだよ団長' in message.content:
      await client.send_message(message.channel, "止まるんじゃねえぞ ってスーちゃんが言ってたけどなんのこと？")
    if 'FGOイベント効率' in message.content:
      await client.send_message(message.channel, "konさんに聞いたほうが早いと思うよ https://twitter.com/niconikon01")

def load_config():
  with open(CONFIG_FILE, "r") as conf:
    settings = yaml.load(conf)
    return settings

def get_google_credentials():
  settings = load_config()
  with open("./config/"+settings["google"]) as google_conf:
    google_json = json.load(google_conf)
    if google_json["private_key"] == 'dummy':
      google_json["private_key"] = os.environ["GOOGLE_PRIVATE_KEY"]
    return ServiceAccountCredentials.from_json_keyfile_dict(google_json, ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])

def get_game_events():
  credentials = get_google_credentials()
  gsc = gspread.authorize(credentials)
  sheet = gsc.open('ソシャゲイベント一覧').sheet1
  return sheet.get_all_records(False, 1)

def get_game_events_text(message):
  event_list = get_game_events()
  text = ""
  for event_data in event_list:
    text += event_data['ソシャゲ名'] + " の " + event_data['イベント名'] + " は " + event_data['イベント終了'] + " まで\n"
  return text + "だよ"

# 設定ファイル読み込み
try:
  with open("./config/secret_conf.yml", "r") as secret_conf:
    settings = yaml.load(secret_conf)
    os.environ["DISCORD_ACCESS_TOKEN"] = settings["token"]
    os.environ["MASTER_MAIL_ADDRESS"] = settings["mail"]
except FileNotFoundError:
  print('secret_conf.ymlがないよ')

token = os.environ["DISCORD_ACCESS_TOKEN"]
client.run(token)
