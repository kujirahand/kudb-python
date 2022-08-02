# kudb functions

## change_db(filename = ':memory:', table_name = 'kudb')

Change Database



## clear(file=None)

clear doc and key-value-store


```
>>> clear(file=MEMORY_FILE)
>>> insert_many([1,2,3,4,5])
>>> count_doc()
5
>>> clear_doc()
>>> count_doc()
0
```



## clear_doc(file=None)

clear all doc


```
>>> clear(file=MEMORY_FILE)
>>> insert_many([1,2,3,4,5])
>>> count_doc()
5
>>> clear_doc()
>>> count_doc()
0
```



## clear_keys()

clear all keys



## close()

close database



## connect(filename = ':memory:', table_name='kudb')

Connect to database



## delete(id=None, key=None, file=None)

delete by id or key

```
>>> clear(file=MEMORY_FILE)
>>> insert_many([1,2,3])
>>> delete(id=3)
>>> [a for a in get_all()]
[1, 2]
>>> clear()
>>> set_key('Taro', 30)
>>> set_key('Jiro', 18)
>>> delete(key='Taro')
>>> list(get_keys())
['Jiro']
```



## delete_key(key)

delete key



## find(callback, limit=None)

find doc by lambda

```
>>> clear(file=MEMORY_FILE)
>>> insert_many([{"name": "Taro", "age":30},{"name": "Bob", "age":19},{"name": "Coo", "age": 21}])
>>> [a['name'] for a in find(lambda v: v['age'] == 19)]
['Bob']
>>> [a['name'] for a in find(lambda v: v['age'] < 22)]
['Bob', 'Coo']
>>> clear()
>>> insert_many([1,2,3,4,5])
>>> [v for v in find(lambda c: c>=2, limit=3)]
[2, 3, 4]
```



## get(id=None, key=None, file=None)

get doc by id or key

```
>>> clear(file=MEMORY_FILE)
>>> insert_many([{'name': 'A'},{'name': 'B'},{'name': 'C'}])
>>> get(id=1)['name']
'A'
```



## get_all(limit=None, order_asc=True, from_id=None, file=None)

get all doc

```
>>> clear(file=MEMORY_FILE)
>>> insert_many([{'name':'A'},{'name':'B'},{'name':'C'},{'name':'D'}])
>>> [a['name'] for a in get_all()]
['A', 'B', 'C', 'D']
>>> [a['name'] for a in get_all(limit=2)]
['A', 'B']
>>> [a['name'] for a in get_all(limit=2,from_id=3)]
['C', 'D']
>>> [a['name'] for a in get_all(order_asc=False)]
['D', 'C', 'B', 'A']
>>> [a['name'] for a in get_all(limit=2,order_asc=False)]
['D', 'C']
```



## get_by_id(id, def_value=None, file=None)

get doc by id

```
>>> clear(file=MEMORY_FILE)
>>> insert_many( [{'name': 'A'}, {'name': 'B'}, {'name': 'C'}] )
>>> get_by_id(1)['name']
'A'
>>> get_by_id(5, 'ne')
'ne'
```



## get_info(key, default = '')

get data and info



## get_key(key, default = '', file=None)

get data by key


```
>>> _ = connect()
>>> set_key('Jiro', 30)
>>> get_key('Jiro')
30
>>> set_key('Jiro', 31)
>>> get_key('Jiro')
31
>>> set_key('Sabu', 18)
>>> get_key('hoge', 'ne')
'ne'
>>> close()
>>> set_key('fuga', 123, file=MEMORY_FILE)
>>> get_key('fuga', file=MEMORY_FILE)
123
```



## get_keys(clear_cache = True)

get keys

```
>>> _ = connect()
>>> clear()
>>> set_key('Ako', 19)
>>> set_key('Iko', 20)
>>> sorted(list(get_keys()))
['Ako', 'Iko']
```



## insert(values, file=None)

insert doc

```
>>> clear(file=MEMORY_FILE)
>>> insert({'name':'A'})
1
>>> insert({'name':'B'})
2
>>> [a['name'] for a in get_all()]
['A', 'B']
```



## insert_many(value_list, file=None)

insert many doc

```
>>> clear(file=MEMORY_FILE)
>>> insert_many([1,2,3,4,5])
>>> get_by_id(1)
1
>>> get_by_id(2)
2
```



## kvs_json()

dump key-value items to json



## recent(limit=100, offset=0)

get recent docs

```
>>> clear(file=MEMORY_FILE)
>>> insert_many( [{'name': 'A'}, {'name': 'B'}, {'name': 'C'}] )
>>> [a['name'] for a in recent(2)]
['C', 'B']
>>> clear(file=MEMORY_FILE)
>>> insert_many( [1,2,3,4,5] )
>>> [v for v in recent(3)]
[5, 4, 3]
>>> [v for v in recent(limit=3, offset=3)]
[2, 1]
```



## set_key(key, value, file=None)

set data by key

```
>>> set_key('hoge', 30, file=':memory:')
>>> get_key('hoge')
30
>>> set_key(1, 40)
>>> get_key(1)
40
```



## update(doc_id, values)

update doc

```
>>> clear(file=MEMORY_FILE)
>>> insert_many([1,2,3,4,5])
>>> get_by_id(1)
1
>>> update(1, 100)
>>> get_by_id(1)
100
```



