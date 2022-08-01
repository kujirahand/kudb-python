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

## Simple sample

document database sample:

```simple-doc.py
import kudb

# connect to file database
kudb.connect('test.db')

# insert
kudb.insert({'name': 'Tako', 'age': 18})
kudb.insert({'name': 'Ika', 'age': 19})

# get data
for row in kudb.get_all():
    print(row)

# get data by id
print(kudb.get(id=1)) # show 1st row

# close
kudb.close()
```

key-value store sample:

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

# functions

- [/docs/functions.md](https://github.com/kujirahand/kudb-python/blob/main/docs/functions.md)

