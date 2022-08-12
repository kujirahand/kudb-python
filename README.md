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
import kudb, json

# connect to file database
kudb.connect('test.db')

# insert
kudb.insert({'name': 'Tako', 'age': 18}, tag='name')
kudb.insert({'name': 'Ika', 'age': 19})
kudb.insert({'name': 'Poko', 'age': 12})
kudb.insert({'name': 'Foo', 'age': 13})

# insert_many
kudb.insert_many([{"name": "A", "age": 10},{"name": "B", "age": 11},{"name": "C", "age": 12}], tag='name')

# get data
for row in kudb.get_all():
    print(row) # all

# get recent
for row in kudb.recent(2):
    print(row) # => B and C

# get data by id
print(kudb.get(id=1)) # => Tako

# find by lambda
print(json.dumps(kudb.find(lambda v: v['name']=='Ika'))) # => Ika

# find by keys
print(json.dumps(kudb.find(keys={"name": "Ika"}))) # => Ika
print(json.dumps(kudb.find(keys={"age": 19}))) # => Ika

# get by tag
print(kudb.get(tag="Ika")[0]) # => Ika

# close
kudb.close()
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
