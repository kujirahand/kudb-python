# kudb

ドキュメント指向の簡易データベース。

## 概要

- シンプルで便利なドキュメント指向データベースとキー・バリューストア
- インストールが簡単(SQLiteをバックエンドに利用するので便利)

## インストール方法

```
$ python3 -m pip install kudb
```

## リポジトリ

- [(GitHub) github.com/kujirahand/kudb-python](https://github.com/kujirahand/kudb-python)
- [(PyPI) pypi.org/project/kudb/](https://pypi.org/project/kudb/)

# ドキュメント

- [/README.md](https://github.com/kujirahand/kudb-python/blob/main/README.md)
- [/docs/README_ja.md](https://github.com/kujirahand/kudb-python/blob/main/docs/README_ja.md)
- [/docs/functions.md](https://github.com/kujirahand/kudb-python/blob/main/docs/functions.md)

## 使い方

- (1) データベースに接続 --- kudb.connect()
- (2) データ挿入や更新、検索
  - データの追加 --- kudb.insert()
  - データの更新 --- kudb.update()
  - データの取得 --- kudb.get_all() / kudb.get()
  - データの削除 --- kudb.delete()
- (3) データベースを閉じる --- kudb.close()
- [メソッドの一覧](https://github.com/kujirahand/kudb-python/blob/main/docs/functions.md)


## 基本的なサンプル

一番簡単な使い方は次の通りです。

```sample-basic.py
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
```

## 簡単な検索

保存したデータを検索するには、次のようなプログラムを記述します。

```sample-find.py
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
```

## タグを指定して検索

検索用のタグを指定すると高速に検索できます。
タグを指定すると、更新や削除が容易です。

```sample-tag.py
import kudb
kudb.connect('test.db')
kudb.clear()

# タグを指定してデータの挿入(タグを指定すると検索が速くなる)
kudb.insert({'name': 'Tako', 'age': 18}, tag='Tako')
kudb.insert({'name': 'Ika', 'age': 19}, tag='Ika')
kudb.insert({'name': 'Poko', 'age': 12}, tag='Poko')

# タグを指定してデータを取得
print('tag=Ika =>', kudb.get(tag='Ika')[0])

# タグを指定してデータの一括挿入
kudb.insert_many([
    {"name": "A", "age": 10},
    {"name": "B", "age": 11},
    {"name": "C", "age": 12}], tag_name='name')

# タグを指定してデータを取得
print('tag=B =>', kudb.get(tag='B')[0])

# IDを指定してデータを抽出(一番高速に抽出可能)
print('id=1 =>', kudb.get(id=1)) # => Tako

# タグを指定して抽出(それなりに高速に抽出)
for row in kudb.get(tag="Ika"):
    print('tag=Ika =>', row) # Ika

# キーを指定して抽出
for row in kudb.find(keys={"name": "Ika"}): # nameがIkaのものを列挙
    print('find.keys={name:ika} => ', row) # Ika
for row in kudb.find(keys={"age": 19}): # ageが19のものを列挙
    print('find.keys={age:19} => ',row) # 19 (Ika)

# lambda関数を指定してデータを抽出
for row in kudb.find(lambda v: v['name'] == 'Ika'): # nameがIkaのものを列挙
    print('lambda.name=Ika =>', row) # => Ika
for row in kudb.find(lambda v: v['age'] >= 12): # ageが12以上のものを列挙
    print('lambda.age=12 =>', row) # => Ika
```

## 更新と削除

データの更新と削除は次の通りです。

```sample-update.py
import kudb
kudb.connect('test.db')
kudb.clear()

# データの挿入
kudb.insert_many([
    {"name": "A", "age": 10},
    {"name": "B", "age": 11},
    {"name": "C", "age": 12},
    {"name": "D", "age": 13},
    {"name": "E", "age": 14}], tag_name='name')

# Eを削除(idを指定)
kudb.delete(id=5)

# Cを削除(tagを指定)
kudb.delete(tag='C')

# データの更新(idを指定)
kudb.update_by_id(1, {'name': 'A', 'age': 22})
print('update.A=22 >', kudb.get(id=1))

# データの更新(tagを指定)
kudb.update_by_tag('B', {'name': 'B', 'age': 23})
print('update.B=23 >', kudb.get(tag='B'))
```

### キー・バリューストアの使い方

Key-Valueストアとしても利用できます。

```sample-kvs.py
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
```

