import kudb

# DBに接続
kudb.connect('test.db')

# キー「hoge」に1234を設定
kudb.set_key('hoge', 1234)

# キー「hoge」を取得
print(kudb.get_key('hoge'))

# 存在しないキーを抽出
print(kudb.get_key('hoge_1st', 'not exists'))

# 閉じる
kudb.close()

