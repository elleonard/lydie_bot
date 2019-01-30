# これは何？

身内用に使ってるdiscord botのリディーちゃんです

# 機能

## イベントいつまで？

彼女にメンションで `イベントいつまで？` と聞くと、spreadsheetに登録されたイベント情報を返してくれます。
ローカルで試したい場合にはサービスアカウントを作ったりいろいろしてください。

## 止まるんじゃねえぞ

彼女にメンションで `何やってんだよ団長` と聞いてみてください。

# デプロイ方法

```
git push heroku master
```

# ローカルでの実行方法

`secret_conf.yml` にdiscordのアクセストークンを記述するか
環境変数 `DISCORD_ACCESS_TOKEN` にdiscordのアクセストークンを登録した状態で

```
py -3 lydie.py ./config/config_local.yml
```

