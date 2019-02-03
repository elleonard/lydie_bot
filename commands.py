
class Command():
  def __init__(self, text, help):
    self.text = text
    self.help = help

EVENT_SCHEDULE = Command("イベントいつまで？", "ゲームのイベントがいつまでか教えてあげる")
ORUGA_ITSUKA = Command("何やってんだよ団長", "スーちゃんがなんだかウズウズしてる")
FGO_EVENT = Command("FGOイベント効率", "konさんに聞いてね")
HELP = Command("help", "コマンド一覧を表示するよ")
SPREADSHEET = Command("シートどこ？", "spreadsheetのURLを返すよ")
BARREL = Command("たーる", "たるですよ")
MONSTER_HUNTER = Command("何狩る？", "狩るモンスターに迷ったら占うよ。種族とか場所指定もできるよ 例「何狩る？ 飛竜種 獣竜種 陸珊瑚の台地 古代樹の森」")
ASROC_YONEKURA = Command("そんなに僕たちの力が見たいのか", "スーちゃんがよく見てる動画貼っておくね")

list = [
  EVENT_SCHEDULE, ORUGA_ITSUKA, ASROC_YONEKURA, FGO_EVENT, MONSTER_HUNTER, SPREADSHEET, BARREL, HELP
]
