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

## 使い方

- (1) データベースに接続 --- kudb.connect()
- (2) データ挿入や更新、検索など --- kudb.insert() / kudb.update() / kudb.get_all()
- (3) データベースを閉じる --- kudb.close()

## サンプル

一番簡単な使い方は次の通りです。

```simple-doc.py
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
    print(row) # all

# データベースを閉じる
kudb.close()
```

データの検索や抽出は次のように記述します。

```simple-doc2.py
import kudb

# データベースへの接続
kudb.connect('test.db')

# 全部のデータをクリア
kudb.clear()

# タグを指定してデータの挿入(タグを指定すると検索が速くなる)
kudb.insert({'name': 'Tako', 'age': 18}, tag='name')
kudb.insert({'name': 'Ika', 'age': 19})
kudb.insert({'name': 'Poko', 'age': 12})

# タグを指定してデータの一括挿入
kudb.insert_many([
    {"name": "A", "age": 10},
    {"name": "B", "age": 11},
    {"name": "C", "age": 12}], tag='name')

# 最後に挿入した2件を取り出す場合
for row in kudb.recent(2):
    print(row) # => B and C

# IDを指定してデータを抽出(一番高速に抽出可能)
print(kudb.get(id=1)) # => Tako

# タグを指定して抽出(それなりに高速に抽出)
for row in kudb.get(tag="Ika"):
    print(row) # Ika

# キーを指定して抽出
for row in kudb.find(keys={"name": "Ika"}): # nameがIkaのものを列挙
    print(row) # Ika
for row in kudb.find(keys={"age": 19}): # ageが19のものを列挙
    print(row) # 19 (Ika)

# lambda関数を指定してデータを抽出
for row in kudb.find(lambda v: v['name'] == 'Ika'): # nameがIkaのものを列挙
    print(row) # => Ika
for row in kudb.find(lambda v: v['age'] >= 12): # ageが12以上のものを列挙
    print(row) # => Ika

# データベースを閉じる
kudb.close()
```

データの更新と削除は次の通りです。

```simple-doc2.py
import kudb

# データベースへの接続
kudb.connect('test.db')
# 全部クリア
kudb.clear()

# データの挿入
kudb.insert({'name': 'Tako', 'age': 18}, tag='name')
kudb.insert({'name': 'Ika', 'age': 19})
kudb.insert({'name': 'Poko', 'age': 12})
kudb.insert({'name': 'Foo', 'age': 13})

# Ikaを削除(idを指定)
kudb.delete(id=2)

# Fooを削除(tagを指定)
kudb.delete(tag='Foo')

# データの更新(idを指定)
kudb.update_by_id(1, {'name': 'Tako', 'age': 22})
print(kudb.get(id=1))

# データの更新(tagを指定)
kudb.update_by_tag('Tako', {'name': 'Tako', 'age': 23})
print(kudb.get(tag='Tako'))

# データを全部表示
print("--- all ---")
for row in kudb.get_all():
    print(row)
```


### キー・バリューストアの使い方

Key-Valueストアとしても利用できます。

```simple-kvs.py
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

# Documents

- [/docs/functions.md](https://github.com/kujirahand/kudb-python/blob/main/docs/functions.md)
- [/docs/README_ja.md](https://github.com/kujirahand/kudb-python/blob/main/docs/README_ja.md)

