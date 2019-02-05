import random
from distutils.util import strtobool
import gspread
import config

MONSTER_TYPES = ['牙竜種', '鳥竜種', '獣竜種', '魚竜種', '飛竜種', '古龍種']
MONSTER_HUNTER_AREAS = ['古代樹の森', '大蟻塚の荒地', '陸珊瑚の台地', '瘴気の谷', '龍結晶の地', '特殊エリア']

def get_monster(text):
  monster_list = get_monster_list()
  # 対象となる種族
  monster_types = []
  for monster_type in MONSTER_TYPES:
    if monster_type in text:
      monster_types.append(monster_type)
  if len(monster_types) == 0:
    monster_types = MONSTER_TYPES
  # 対象となるエリア
  areas = []
  for area in MONSTER_HUNTER_AREAS:
    if area in text:
      areas.append(area)
  if len(areas) == 0:
    areas = MONSTER_HUNTER_AREAS
  target_monsters = []
  for monster in monster_list:
    if is_target_monster(monster, monster_types, areas):
      target_monsters.append(monster)
  if len(target_monsters) == 0:
    return "条件に合う子がいないみたい"
  monster = random.choice(target_monsters)
  return monster['モンスター名']+" にしよう"

def is_target_monster(monster, types, areas):
  is_target = False
  for area in areas:
    is_target |= strtobool(monster[area])
  return is_target & (monster['種族'] in types)

def get_monster_list():
  credentials = config.get_google_credentials()
  gsc = gspread.authorize(credentials)
  sheet = gsc.open('MHW 大型モンスター一覧').sheet1
  return sheet.get_all_records(False, 1)
