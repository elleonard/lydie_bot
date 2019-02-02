import yaml
import json
import os
import sys

from oauth2client.service_account import ServiceAccountCredentials

args = sys.argv

CONFIG_FILE = "./config/config.yml" if len(args) < 2 else args[1]

# 設定ファイル読み込み
try:
  with open("./config/secret_conf.yml", "r") as secret_conf:
    settings = yaml.load(secret_conf)
    os.environ["DISCORD_ACCESS_TOKEN"] = settings["token"]
    os.environ["MASTER_MAIL_ADDRESS"] = settings["mail"]
    os.environ["SPREADSHEET_EVENT"] = settings["spreadsheet"]["event"]
    os.environ["SPREADSHEET_MONSTER_HUNTER"] = settings["spreadsheet"]["monster_hunter"]
except FileNotFoundError:
  print('secret_conf.ymlがないよ')

token = os.environ["DISCORD_ACCESS_TOKEN"]

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
