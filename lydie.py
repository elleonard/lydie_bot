import discord
import yaml
import json
import os
import sys
import random
from distutils.util import strtobool

import gspread

import config
import commands
import monster_hunter
import game_event

client = discord.Client()


@client.event
async def on_ready():
  print('こんにちはー！')

@client.event
async def on_message(message):
  if client.user in message.mentions:
    if commands.EVENT_SCHEDULE.text in message.content:
      await message.channel.send(game_event.get_game_events_text())
    if commands.ORUGA_ITSUKA.text in message.content:
      await message.channel.send("止まるんじゃねえぞ ってスーちゃんが言ってたけどなんのこと？")
    if commands.ASROC_YONEKURA.text in message.content:
      await message.channel.send("https://www.nicovideo.jp/watch/sm14950071")
    if commands.FGO_EVENT.text in message.content:
      await message.channel.send("konさんに聞いたほうが早いと思うよ https://twitter.com/niconikon01")
    if commands.SPREADSHEET.text in message.content:
      await message.channel.send("ここだよ\n"+get_spreadsheet_urls())
    if commands.BARREL.text in message.content:
      await message.channel.send(get_barrel())
    if commands.MONSTER_HUNTER.text in message.content:
      await message.channel.send(monster_hunter.get_monster(message.content))
    if commands.HELP.text in message.content:
      await message.channel.send(get_help_text())

def get_barrel():
  rand = random.randint(0,2)
  if rand == 0:
    return 'たるですよ'
  if rand == 1:
    return 'たるだけに最近たるんで……な、なんでもない！'
  return 'たーる'

def get_help_text():
  help_text = "コマンド一覧\n"
  for command in commands.list:
    help_text += command.text+": "+command.help+"\n"
  return help_text

def get_spreadsheet_urls():
  return "イベントいつまで: " + os.environ["SPREADSHEET_EVENT"] + "\n何狩る？: " + os.environ["SPREADSHEET_MONSTER_HUNTER"]

client.run(os.environ["DISCORD_ACCESS_TOKEN"])
