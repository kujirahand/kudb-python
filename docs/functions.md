# kudb functions

## change_db(filename: str = ":memory:", table_name: str = "kudb") -> None

Change Database



## clear(file: Optional[str] = None) -> None

clear doc and key-value-store


```py
>>> clear(file=MEMORY_FILE)
>>> insert_many([1,2,3,4,5])
>>> count_doc()
5
>>> clear_doc()
>>> count_doc()
0
```



## clear_doc(file: Optional[str] = None) -> None

clear all doc


```py
>>> clear(file=MEMORY_FILE)
>>> insert_many([1,2,3,4,5])
>>> count_doc()
5
>>> clear_doc()
>>> count_doc()
0
```



## clear_keys() -> None

clear all keys



## close() -> None

close database



## connect(filename: str = ":memory:", table_name: str = "kudb") -> sqlite3.Connection

Connect to database



## count_doc(file: Optional[str] = None) -> int

count doc


```py
>>> clear(file=MEMORY_FILE)
>>> insert_many([{"name": "A"},{"name": "B"},{"name": "C"}])
>>> count_doc()
3
```



## delete(id: Optional[int] = None, key: Optional[str] = None, tag: Optional[str] = None, doc_keys: Optional[Dict[str, Any]] = None, file: Optional[str] = None) -> None

delete by id or key

```py
>>> clear(file=MEMORY_FILE)
>>> insert_many([1,2,3])
>>> delete(id=3)
>>> [a for a in get_all()]
[1, 2]
```


delete key in key-value store:
```py
>>> clear()
>>> set_key('Taro', 30)
>>> set_key('Jiro', 18)
>>> delete(key='Taro')
>>> list(get_keys())
['Jiro']
```


delete doc_keys in docs
```py
>>> clear()
>>> insert_many([{'name': 'A'},{'name': 'B'},{'name': 'C'}])
>>> delete(doc_keys={'name': 'A'})
>>> len(get_all())
2
>>> clear()
>>> insert_many([{'name': 'A', 'age': 30},{'name': 'B', 'age': 31},{'name': 'C', 'age': 32}])
>>> delete(doc_keys={'name': 'A', 'age': 30}) # delete
>>> len(get_all())
2
>>> delete(doc_keys={'name': 'B', 'age': 3}) # not delete any data
>>> len(get_all())
2
```



## delete_key(key: str) -> None

delete key



## find( callback: Optional[Callable[[Any], bool]] = None, keys: Optional[Dict[str, Any]] = None, limit: Optional[int] = None, ) -> List[Any]

find doc by lambda

```py
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
>>> clear(file=MEMORY_FILE)
>>> insert_many([{"name": "Taro", "age":30},{"name": "Bob", "age":19},{"name": "Coo", "age": 21}])
>>> find(keys={"name": "Taro"})[0]["age"]
30
>>> find(keys={"age": 30})[0]["name"]
'Taro'
```



## find_one(callback: Optional[Callable[[Any], bool]] = None, keys: Optional[Dict[str, Any]] = None, limit: Optional[int] = None) -> Any

find one doc by lambda

>> clear(file=MEMORY_FILE)
>> insert_many([{'name': 'Taro', 'age': 30}, {'name': 'Jiro', 'age': 18}])
>> find_one(keys={'name': 'Jiro'})['age']
18


## get( id: Optional[int] = None, key: Optional[str] = None, tag: Optional[str] = None, file: Optional[str] = None, ) -> Any

get docs by id or key or tag

```py
>>> clear(file=MEMORY_FILE)
>>> insert_many([{'name': 'A'},{'name': 'B'},{'name': 'C'}], tag_name='name')
>>> get(id=1)['name']
'A'
>>> get(tag='C')[0]['name']
'C'
```



## get_all(limit: Optional[int] = None, order_asc: bool = True, from_id: Optional[int] = None, file: Optional[str] = None) -> List[Any]

get all doc

```py
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



## get_by_id(id: int, def_value: Any = None, file: Optional[str] = None) -> Any

get doc by id

```py
>>> clear(file=MEMORY_FILE)
>>> insert_many( [{'name': 'A'}, {'name': 'B'}, {'name': 'C'}] )
>>> get_by_id(1)['name']
'A'
>>> get_by_id(5, 'ne')
'ne'
```



## get_by_tag(tag: str, limit: Optional[int] = None, file: Optional[str] = None) -> List[Any]

get doc by tag

```py
>>> clear(file=MEMORY_FILE)
>>> insert_many( [{'name': 'A'}, {'name': 'B'}, {'name': 'C'}], tag_name='name' )
>>> get_by_tag('B')[0]['name']
'B'
```



## get_high_score(limit: int = 10, score_key: str = "score") -> List[Any]

get high score docs

```py
>>> clear(file=MEMORY_FILE)
>>> insert_many([{'name': 'A', 'score': 50}, {'name': 'B', 'score': 80}, {'name': 'C', 'score': 70}])
>>> [a['name'] for a in get_high_score(2)]
['B', 'C']
```



## get_info(key: str, default: str = "") -> Any

get data and info



## get_key(key: str, default: Any = "", file: Optional[str] = None) -> Any

get data by key


```py
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



## get_keys(clear_cache: bool = True) -> Any

get keys

```py
>>> _ = connect()
>>> clear()
>>> set_key('Ako', 19)
>>> set_key('Iko', 20)
>>> sorted(list(get_keys()))
['Ako', 'Iko']
```



## get_one(id: Optional[int] = None, tag: Optional[str] = None, file: Optional[str] = None) -> Any

get one doc by id or tag

```py
>>> clear(file=MEMORY_FILE)
>>> insert_many([{'tag': 'A', 'v': 1}, {'tag': 'A', 'v': 2}, {'tag': 'B', 'v': 3}], tag_name='tag')
>>> get_one(tag='A')['v']
1
```



## get_tag_name(def_tag_name: str = "tag") -> Any

get tag name



## insert(value: Any, file: Optional[str] = None, tag_name: Optional[str] = None, tag: Optional[str] = None) -> Optional[int]

insert doc

```py
>>> clear(file=MEMORY_FILE)
>>> insert({'name':'A'})
1
>>> insert({'name':'B'})
2
>>> [a['name'] for a in get_all()]
['A', 'B']
```


insert doc with tag
```py
>>> clear()
>>> insert({'name':'banana', 'price': 30}, tag='banana')
1
>>> get_by_tag("banana")[0]['price']
30
```



## insert_many(value_list: List[Any], file: Optional[str] = None, tag_name: Optional[str] = None) -> None

insert many doc

```py
>>> clear(file=MEMORY_FILE)
>>> insert_many([1,2,3,4,5])
>>> get_by_id(1)
1
>>> get_by_id(2)
2
```



## insert_score(score: int, name: str, meta: Optional[Dict[str, Any]] = None, score_key: str = "score", file: Optional[str] = None) -> Optional[int]

insert score doc

```py
>>> clear(file=MEMORY_FILE)
>>> insert_score(100, "A")
1
>>> insert_score(200, "B")
2
>>> get_by_id(1)['name']
'A'
>>> get_by_id(2)['name']
'B'
>>> get_high_score(2)[0]['name']
'B'
```



## kvs_json() -> str

dump key-value items to json



## recent(limit: int = 100, offset: int = 0, order_asc: bool = True) -> List[Any]

get recent docs

```py
>>> clear(file=MEMORY_FILE)
>>> insert_many( [{'name': 'A'}, {'name': 'B'}, {'name': 'C'}] )
>>> [a['name'] for a in recent(2)]
['B', 'C']
>>> clear(file=MEMORY_FILE)
>>> insert_many( [1,2,3,4,5] )
>>> [v for v in recent(3)]
[3, 4, 5]
>>> [v for v in recent(limit=3, offset=3)]
[1, 2]
>>> [v for v in recent(limit=3, order_asc=False)]
[5, 4, 3]
```



## set_key(key: str, value: Any, file: Optional[str] = None) -> None

set data by key

```py
>>> set_key('hoge', 30, file=':memory:') # insert
>>> get_key('hoge')
30
>>> set_key(1, 40)
>>> get_key(1)
40
>>> set_key('hoge', 35) # update
>>> get_key('hoge')
35
```



## set_tag_name(tag_name: str) -> None

set tag name



## update(id: Optional[int] = None, new_value: Any = None, tag: Optional[str] = None) -> None

update doc


update by id
```py
>>> clear(file=MEMORY_FILE)
>>> insert_many([1,2,3,4,5])
>>> get_by_id(1)
1
>>> update(1, 100)
>>> get_by_id(1)
100
```


update by id:
```py
>>> clear()
>>> insert_many([{"name": "A", "age": 30}, {"name": "B", "age": 20}], tag_name="name")
>>> update(id=2, new_value={"name":"B", "age": 10})
>>> get_by_tag("B")[0]["age"]
10
```


update by tag:
```py
>>> clear()
>>> insert_many([{"name": "A", "age": 30}, {"name": "B", "age": 20}], tag_name="name")
>>> update(tag="B", new_value={"name":"B", "age": 15})
>>> get_by_tag("B")[0]["age"]
15
```



## update_by_id(id: int, new_value: Any) -> None

update doc value by tag

```py
>>> clear()
>>> insert_many([{"name": "A", "age": 30}, {"name": "B", "age": 20}], tag_name="name")
>>> update_by_tag("B", {"name":"B", "age": 15})
>>> get_by_tag("B")[0]["age"]
15
```



## update_by_tag(tag: str, new_value: Any) -> None

update doc value by tag

```py
>>> clear()
>>> insert_many([{"name": "A", "age": 30}, {"name": "B", "age": 20}], tag_name="name")
>>> update_by_tag("B", {"name":"B", "age": 15})
>>> get_by_tag("B")[0]["age"]
15
```



