# kudb

simple document database for python

## Features

- Simple and convenient Document database and Key-value Store Library
- Easy to install (Use SQLite for the back end)

## Installation

```
$ python3 -m pip install kudb
```

## Repository

- [(GitHub) github.com/kujirahand/kudb-python](https://github.com/kujirahand/kudb-python)
- [(PyPI) pypi.org/project/kudb/](https://pypi.org/project/kudb/)

## Sample for document database

document database sample:

```simple-doc.py
import kudb

# connect to file db
kudb.connect('test.db')

# insert data
kudb.insert({'name': 'Tako', 'age': 18})
kudb.insert({'name': 'Ika', 'age': 19})
kudb.insert({'name': 'Poko', 'age': 12})
kudb.insert({'name': 'Foo', 'age': 13})

# get all data
for row in kudb.get_all():
    print(row) # all

# close db
kudb.close()
```

Sample of finding data:

```simple-doc-find.py
import kudb

# connect to file db
kudb.connect('test.db')

# clear all data
kudb.clear()

# insert with tag / if you set tag then find data speedy
kudb.insert({'name': 'Tako', 'age': 18}, tag='Tako')
kudb.insert({'name': 'Ika', 'age': 19}, tag='Ika')
kudb.insert({'name': 'Poko', 'age': 12}, tag='Poko')

# insert many data with tag
kudb.insert_many([
    {"name": "A", "age": 10},
    {"name": "B", "age": 11},
    {"name": "C", "age": 12}], tag_name='name')

# get recent data
for row in kudb.recent(2):
    print(row) # => B and C

# get data by id (most speedy)
print(kudb.get(id=1)) # => Tako

# get data by tag
for row in kudb.get(tag="Ika"):
    print(row) # Ika

# find data by keys
for row in kudb.find(keys={"name": "Ika"}): # enum name=Ika
    print(row) # Ika
for row in kudb.find(keys={"age": 19}): # enum age=19
    print(row) # 19 (Ika)

# find data with lambda
for row in kudb.find(lambda v: v['name'] == 'Ika'): # enum name=Ika
    print(row) # => Ika
for row in kudb.find(lambda v: v['age'] >= 12): # enum age >= 12
    print(row) # => Ika

# close db
kudb.close()
```

Sampe of Updating / Deleteing data:

```samle-doc-update-delete.py
import kudb

# connet to db
kudb.connect('test.db')

# clear all data
kudb.clear()

# insert data with tag
kudb.insert({'name': 'Tako', 'age': 18}, tag_name='name')
kudb.insert({'name': 'Ika', 'age': 19})
kudb.insert({'name': 'Poko', 'age': 12})
kudb.insert({'name': 'Foo', 'age': 13})

# delete by id
kudb.delete(id=2)

# delete by tag
kudb.delete(tag='Foo')

# update by id
kudb.update_by_id(1, {'name': 'Tako', 'age': 22})
print(kudb.get(id=1))

# update by tag
kudb.update_by_tag('Tako', new_value={'name': 'Tako', 'age': 23})
print(kudb.get(tag='Tako'))

# show all data
print("--- all ---")
for row in kudb.get_all():
    print(row)
```

### Sample for key-value-store

```simple-kvs.py
import kudb

# connect to file database
kudb.connect('test.db')

# set_key
kudb.set_key('hoge', 1234)

# get_key
print(kudb.get_key('hoge'))
# get default value
print(kudb.get_key('hoge_1st', 'not exists'))

# close
kudb.close()
```

# Documents

- [/docs/functions.md](https://github.com/kujirahand/kudb-python/blob/main/docs/functions.md)
- [/docs/README_ja.md](https://github.com/kujirahand/kudb-python/blob/main/docs/README_ja.md)
