import discord
import yaml
import os

client = discord.Client()

event_file = 'event.txt'

@client.event
async def on_ready():
  print('こんにちはー！')

@client.event
async def on_message(message):
  if client.user.id in message.content:
    if 'イベントいつまで？' in message.content:
      with open(event_file, encoding = "utf-8") as f:
        lines = [s.strip() for s in f.readlines()]
        for line in lines:
          parts = line.split(",")
          text = parts[0]+"の"+parts[1]+"は"+parts[2]+"まで"
          await client.send_message(message.channel, text)
      await client.send_message(message.channel, "だよ")
    if '何やってんだよ団長' in message.content:
      await client.send_message(message.channel, "止まるんじゃねえぞ ってスーちゃんが言ってたけどなんのこと？")

try:
  with open("secret_conf.yml", "r") as secret_conf:
    settings = yaml.load(secret_conf)
    os.environ["DISCORD_ACCESS_TOKEN"] = settings["token"]
except FileNotFoundError:
  print('secret_conf.ymlがないよ')

token = os.environ["DISCORD_ACCESS_TOKEN"]
client.run(token)
