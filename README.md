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

# Documents

- [/README.md](https://github.com/kujirahand/kudb-python/blob/main/README.md)
- [/docs/README_ja.md](https://github.com/kujirahand/kudb-python/blob/main/docs/README_ja.md)
- [/docs/functions.md](https://github.com/kujirahand/kudb-python/blob/main/docs/functions.md)

## Usage

- (1) connect to database --- kudb.connect()
- (2) CRUD
  - insert data --- kudb.insert()
  - update data --- kudb.update()
  - get data --- kudb.get_all() / kudb.get()
  - delete data --- kudb.delete()
- (3) close --- kudb.close()
- [functions](https://github.com/kujirahand/kudb-python/blob/main/docs/functions.md)


## Basic Sample

Basic sample

```sample-basic.py
import kudb

kudb.connect('test.db')

# insert data
kudb.insert({'name': 'Tako', 'age': 18})
kudb.insert({'name': 'Ika', 'age': 19})
kudb.insert({'name': 'Poko', 'age': 12})
kudb.insert({'name': 'Foo', 'age': 13})

# get all data
for row in kudb.get_all():
    print('get_all >', row) # all

# close
kudb.close()
```

## Find data

Find data

```sample-find.py
import kudb
kudb.connect('test.db')

# clear all data
kudb.clear()

# insert many data
kudb.insert_many([
    {'name': 'Tako', 'age': 18},
    {'name': 'Ika', 'age': 19},
    {'name': 'Hirame', 'age': 20},
])

# get by id
print('id=2 >', kudb.get(id=2))

# find by keys
for row in kudb.find(keys={'name': 'Tako'}):
    print('name=Tako >', row)

# find by lambda
for row in kudb.find(lambda v: v['name'] == 'Tako'):
    print('name=Tako >', row)

# get recent data
for row in kudb.recent(2):
    print('recent(2) =>', row) # => Ika, Hirame
```

## Search data with tag

The doc data can set tag.
When use data with tag, you can search data quickly.
And use data with tag, you can update/delete data quickly.

```sample-tag.py
import kudb
kudb.connect('test.db')
kudb.clear()

# insert data with tag
kudb.insert({'name': 'Tako', 'age': 18}, tag='Tako')
kudb.insert({'name': 'Ika', 'age': 19}, tag='Ika')
kudb.insert({'name': 'Poko', 'age': 12}, tag='Poko')

# get data by tag
print('tag=Ika =>', kudb.get(tag='Ika')[0])

# insert many data with tag_name
kudb.insert_many([
    {"name": "A", "age": 10},
    {"name": "B", "age": 11},
    {"name": "C", "age": 12}], tag_name='name')

# get data by tag
print('tag=B =>', kudb.get(tag='B')[0])

# get data by id (most speedy)
print('id=1 =>', kudb.get(id=1)) # => Tako

# get data by tag
for row in kudb.get(tag="Ika"):
    print('tag=Ika =>', row) # Ika

# find data with keys
for row in kudb.find(keys={"name": "Ika"}): # enum data when name=Ika
    print('find.keys={name:ika} => ', row) # Ika
for row in kudb.find(keys={"age": 19}): # enum data when age=19
    print('find.keys={age:19} => ',row) # 19 (Ika)

# find data with lambda function
for row in kudb.find(lambda v: v['name'] == 'Ika'): # enum data when name=Ika
    print('lambda.name=Ika =>', row) # => Ika
for row in kudb.find(lambda v: v['age'] >= 12): # enum data when age >= 12
    print('lambda.age=12 =>', row) # => Ika
```

## Update and delete

Update and delete sample:

```sample-update.py
import kudb
kudb.connect('test.db')
kudb.clear()

# insert many data with tag_name
kudb.insert_many([
    {"name": "A", "age": 10},
    {"name": "B", "age": 11},
    {"name": "C", "age": 12},
    {"name": "D", "age": 13},
    {"name": "E", "age": 14}], tag_name='name')

# delete by id
kudb.delete(id=5)

# delete by tag
kudb.delete(tag='C')

# update data by id
kudb.update_by_id(1, {'name': 'A', 'age': 22})
print('update.A=22 >', kudb.get(id=1))

# update dagta by tag
kudb.update_by_tag('B', {'name': 'B', 'age': 23})
print('update.B=23 >', kudb.get(tag='B'))
```

### Key-Value Store

Key-Value Store sample:

```sample-kvs.py
import kudb

kudb.connect('test.db')

kudb.set_key('hoge', 1234)
print(kudb.get_key('hoge'))

# get data that does not exists
print(kudb.get_key('hoge_1st', 'not exists'))

kudb.close()
```


