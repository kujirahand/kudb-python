import kudb
kudb.connect('test.db')

# 全部のデータをクリア
kudb.clear()

# データの一括挿入
kudb.insert_many([
    {'name': 'Tako', 'age': 18},
    {'name': 'Ika', 'age': 19},
    {'name': 'Hirame', 'age': 20},
])

# IDを指定してデータを取得
print('id=2 >', kudb.get(id=2))

# データを検索 (keys)
for row in kudb.find(keys={'name': 'Tako'}):
    print('name=Tako >', row)

# データを検索 (lambda)
for row in kudb.find(lambda v: v['name'] == 'Tako'):
    print('name=Tako >', row)

# 最後に挿入した2件を取り出す場合
for row in kudb.recent(2):
    print('recent(2) =>', row) # => Ika, Hirame

