
class Command():
  def __init__(self, text, help):
    self.text = text
    self.help = help

EVENT_SCHEDULE = Command("イベントいつまで？", "ゲームのイベントがいつまでか教えてあげる")
ORUGA_ITSUKA = Command("何やってんだよ団長", "スーちゃんがなんだかウズウズしてる")
FGO_EVENT = Command("FGOイベント効率", "konさんに聞いてね")
HELP = Command("help", "コマンド一覧を表示するよ")
SPREADSHEET = Command("シートどこ？", "spreadsheetのURLを返すよ")

list = [
  EVENT_SCHEDULE, ORUGA_ITSUKA, FGO_EVENT, SPREADSHEET, HELP
]
