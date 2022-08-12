import kudb

# データベースへの接続
kudb.connect('test.db')

# データの挿入
kudb.insert({'name': 'Tako', 'age': 18})
kudb.insert({'name': 'Ika', 'age': 19})
kudb.insert({'name': 'Poko', 'age': 12})
kudb.insert({'name': 'Foo', 'age': 13})

# データを全部抽出する
for row in kudb.get_all():
    print('get_all >', row) # all

# データベースを閉じる
kudb.close()
