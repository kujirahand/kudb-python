"""
Simple document database Library

For examples:
>>> _ = connect()
>>> insert(100) # insert value
1
>>> get_by_id(1) # get value
100

Insert document data:
>>> clear()
>>> insert({"name": "Jiro", "age": 18})
1
>>> get_by_id(1)["name"]
'Jiro'

Insert and find:
>>> clear()
>>> insert({"name": "Jiro", "age": 18})
1
>>> insert({"name": "Sabu", "age": 21})
2
>>> find(lambda v: v["age"] >= 20)[0]["name"]
'Sabu'
"""

from typing import Optional, Callable, Any, Dict, List
import sqlite3
import time
import json


class KudbError(Exception):
    """Kudb Error"""


db: Optional[sqlite3.Connection] = None
cache_db: Dict[str, sqlite3.Connection] = {}
CACHE_KEYS: Dict[str, bool] = {}
SQLS: Dict[str, str] = {}
MEMORY_FILE: str = ":memory:"
cur_filename: str = MEMORY_FILE
cur_tablename: str = "kudb"
SQLITE_MAX_INT: int = 9223372036854775807
# SQL template
SQLS_TEMPLATE = {
    # kvs
    "create": """
    CREATE TABLE IF NOT EXISTS __TABLE_NAME__ (
        key_id INTEGER PRIMARY KEY,
        key TEXT UNIQUE,
        value TEXT DEFAULT '',
        ctime INTEGER DEFAULT 0,
        mtime INTEGER DEFAULT 0
    )
    """,
    "select": "SELECT value FROM __TABLE_NAME__ WHERE key=?",
    "select_info": "SELECT * FROM __TABLE_NAME__ WHERE key=?",
    "keys": "SELECT key FROM __TABLE_NAME__",
    "insert": "INSERT INTO __TABLE_NAME__ (key, value, ctime, mtime) VALUES (?, ?, ?, ?)",
    "update": "UPDATE __TABLE_NAME__ SET value=?, mtime=? WHERE key=?",
    "delete": "DELETE FROM __TABLE_NAME__ WHERE key=?",
    "clear": "DELETE FROM __TABLE_NAME__",
    # doc
    "create_doc": """
    CREATE TABLE IF NOT EXISTS doc__TABLE_NAME__ (
        id INTEGER PRIMARY KEY,
        tag TEXT DEFAULT '',
        value TEXT DEFAULT '',
        ctime INTEGER DEFAULT 0,
        mtime INTEGER DEFAULT 0
    )
    """,
    "select_doc": "SELECT value, id FROM doc__TABLE_NAME__",
    "select_doc_desc": "SELECT value, id FROM doc__TABLE_NAME__ WHERE id <= ? ORDER BY id DESC LIMIT ?",
    "select_doc_asc": "SELECT value, id FROM doc__TABLE_NAME__ WHERE id >= ? ORDER BY id ASC LIMIT ?",
    "recent_doc": "SELECT value, id FROM doc__TABLE_NAME__ ORDER BY id DESC LIMIT ? OFFSET ?",
    "get_doc_by_id": "SELECT value, id FROM doc__TABLE_NAME__ WHERE id=?",
    "get_doc_by_tag": "SELECT value, id FROM doc__TABLE_NAME__ WHERE tag=? LIMIT ?",
    "insert_doc": "INSERT INTO doc__TABLE_NAME__ (value, tag, ctime, mtime) VALUES (?, ?, ?, ?)",
    "update_doc": "UPDATE doc__TABLE_NAME__ SET value=?, tag=?, mtime=? WHERE id=?",
    "update_doc_by_tag": "UPDATE doc__TABLE_NAME__ SET value=?, tag=?, mtime=? WHERE tag=?",
    "delete_doc": "DELETE FROM doc__TABLE_NAME__ WHERE id=?",
    "delete_doc_by_tag": "DELETE FROM doc__TABLE_NAME__ WHERE tag=?",
    "clear_doc": "DELETE FROM doc__TABLE_NAME__",
    "count_doc": "SELECT count(id) FROM doc__TABLE_NAME__",
}


def connect(filename: str = ":memory:", table_name: str = "kudb") -> sqlite3.Connection:
    """Connect to database"""
    global SQLS, cur_filename, db, cur_tablename
    # generate sqls
    SQLS = {}
    for key, val in SQLS_TEMPLATE.items():
        SQLS[key] = val.replace("__TABLE_NAME__", table_name)
    # check cache
    if (filename in cache_db) and (cur_tablename == table_name):  # already open?
        db = cache_db[filename]  # use_cache
        cur_filename = filename
        return db
    # connect to sqlite3
    db = sqlite3.connect(filename, check_same_thread=False)
    cache_db[filename] = db
    cur_filename = filename
    cur_tablename = table_name
    try:
        # create table
        db.executescript(SQLS["create"] + ";" + SQLS["create_doc"])
        # make cache keys
        get_keys(True)
        return db
    except Exception as err:
        raise KudbError("could not initalize database file: " + str(err)) from err


def change_db(filename: str = ":memory:", table_name: str = "kudb") -> None:
    """Change Database"""
    connect(filename, table_name)


def close() -> None:
    """close database"""
    global db, cur_filename
    if db is not None:
        db.close()
        del cache_db[cur_filename]
    db = None
    cur_filename = ""


def get_key(key: str, default: Any = "", file: Optional[str] = None) -> Any:
    """
    get data by key

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
    """
    if file is not None:
        connect(file)
    if db is None:
        raise KudbError("please connect before using `get` method.")
    if key not in CACHE_KEYS:
        return default
    cur = db.cursor()
    try:
        sql = SQLS["select"]
        cur.execute(sql, [key])
        values = cur.fetchone()
        if values is None:
            return default
        return json.loads(values[0])
    except Exception as err:
        raise KudbError(
            f"`get_key({key})` could not read database: {str(err)}"
        ) from err
    finally:
        cur.close()


def get_info(key: str, default: str = "") -> Any:
    """get data and info"""
    cur: Optional[sqlite3.Cursor] = None
    if db is None:
        raise KudbError("please connect before using `get` method.")
    if key not in CACHE_KEYS:
        return default
    try:
        cur = db.cursor()
        cur.execute(SQLS["select_info"], [key])
        values = cur.fetchone()
        return values
    except Exception as err:
        raise KudbError("could not read database: " + str(err)) from err
    finally:
        if cur is not None:
            cur.close()


def set_key(key: str, value: Any, file: Optional[str] = None) -> None:
    """
    set data by key
    >>> set_key('hoge', 30, file=':memory:') # insert
    >>> get_key('hoge')
    30
    >>> set_key(1, 40)
    >>> get_key(1)
    40
    >>> set_key('hoge', 35) # update
    >>> get_key('hoge')
    35
    """
    if file is not None:
        connect(file)
    if db is None:
        raise KudbError("please connect before using `set_key` method.")
    try:
        value_json = json.dumps(value, ensure_ascii=False)
        cur = db.cursor()
        if key in CACHE_KEYS:
            cur.execute(SQLS["update"], [value_json, int(time.time()), key])
        else:
            cur.execute(
                SQLS["insert"], [key, value_json, int(time.time()), int(time.time())]
            )
            CACHE_KEYS[key] = True
        cur.close()
        db.commit()
    except Exception as err:
        raise KudbError("database could not write key: " + str(err)) from err


def delete_key(key: str) -> None:
    """delete key"""
    if db is None:
        raise KudbError("please connect before using `delete_key` method.")
    try:
        cur = db.cursor()
        if key in CACHE_KEYS:
            cur.execute(SQLS["delete"], [key])
            del CACHE_KEYS[key]
        cur.close()
        db.commit()
    except Exception as err:
        raise KudbError("database could not delete key: " + str(err)) from err


def set_keys_from_dict(data: Dict[str, Any], file: Optional[str] = None) -> None:
    """
    set multiple keys from dictionary efficiently

    >>> _ = connect()
    >>> clear()
    >>> set_keys_from_dict({'name': 'Taro', 'age': 30, 'city': 'Tokyo'})
    >>> get_key('name')
    'Taro'
    >>> get_key('age')
    30
    >>> get_key('city')
    'Tokyo'
    >>> set_keys_from_dict({'name': 'Jiro', 'score': 100})  # update and insert
    >>> get_key('name')
    'Jiro'
    >>> get_key('score')
    100
    """
    if file is not None:
        connect(file)
    if db is None:
        raise KudbError("please connect before using `set_keys_from_dict` method.")
    if not isinstance(data, dict):
        raise KudbError("data must be a dictionary in `set_keys_from_dict` method.")
    if len(data) == 0:
        return

    try:
        cur = db.cursor()
        current_time = int(time.time())

        # Separate keys for insert and update
        insert_data = []
        update_data = []

        for key, value in data.items():
            value_json = json.dumps(value, ensure_ascii=False)
            if key in CACHE_KEYS:
                update_data.append([value_json, current_time, key])
            else:
                insert_data.append([key, value_json, current_time, current_time])
                CACHE_KEYS[key] = True

        # Batch insert new keys
        if insert_data:
            cur.executemany(SQLS["insert"], insert_data)

        # Batch update existing keys
        if update_data:
            cur.executemany(SQLS["update"], update_data)

        cur.close()
        db.commit()
    except Exception as err:
        raise KudbError("database could not write keys: " + str(err)) from err


def get_keys(clear_cache: bool = True) -> Any:
    """
    get keys
    >>> _ = connect()
    >>> clear()
    >>> set_key('Ako', 19)
    >>> set_key('Iko', 20)
    >>> sorted(list(get_keys()))
    ['Ako', 'Iko']
    """
    global CACHE_KEYS
    if db is None:
        return []
    # Use Cache?
    if clear_cache or len(CACHE_KEYS) == 0:
        cur = db.cursor()
        cur.execute(SQLS["keys"])
        CACHE_KEYS = {}
        for i in cur.fetchall():
            CACHE_KEYS[i[0]] = True
    return CACHE_KEYS.keys()


def kvs_json() -> str:
    """dump key-value items to json"""
    obj = {}
    for key in get_keys():
        obj[key] = get_key(key)
    return json.dumps(obj, ensure_ascii=False)


def clear_keys() -> None:
    """clear all keys"""
    global CACHE_KEYS
    if db is None:
        raise KudbError("please connect before using `clear_keys` method.")
    try:
        cur = db.cursor()
        cur.execute(SQLS["clear"])
        CACHE_KEYS = {}
        cur.close()
        db.commit()
    except Exception as err:
        raise KudbError("could not read database: " + str(err)) from err


def count_doc(file: Optional[str] = None) -> int:
    """
    count doc

    >>> clear(file=MEMORY_FILE)
    >>> insert_many([{"name": "A"},{"name": "B"},{"name": "C"}])
    >>> count_doc()
    3
    """
    if file is not None:
        connect(file)
    if db is None:
        raise KudbError("please connect before using `count_doc` method.")
    try:
        cur = db.cursor()
        cur.execute(SQLS["count_doc"])
        val = cur.fetchone()
        return val[0]
    except Exception as err:
        raise KudbError("could not count docs:" + str(err)) from err


def get_all(
    limit: Optional[int] = None,
    order_asc: bool = True,
    from_id: Optional[int] = None,
    file: Optional[str] = None,
) -> List[Any]:
    """
    get all doc
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
    """
    # check parameters
    if file is not None:
        connect(file)
    if db is None:
        raise KudbError("please connect before using `get_all` method.")
    if limit is None:
        limit = count_doc()
    sql = SQLS["select_doc_asc"]
    if order_asc:
        if from_id is None:
            from_id = 1
    else:
        sql = SQLS["select_doc_desc"]
        if from_id is None:
            from_id = SQLITE_MAX_INT
    # select doc
    result = []
    cur = db.cursor()
    for row in cur.execute(sql, [from_id, limit]):
        values = json.loads(row[0])
        if isinstance(values, dict):
            values["id"] = row[1]
        result.append(values)
    cur.close()
    return result


def recent(limit: int = 100, offset: int = 0, order_asc: bool = True) -> List[Any]:
    """
    get recent docs
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
    """
    if db is None:
        raise KudbError("please connect before using `recent` method.")
    cur = db.cursor()
    result = []
    for row in cur.execute(SQLS["recent_doc"], [limit, offset]):
        values = json.loads(row[0])
        if isinstance(values, dict):
            values["id"] = row[1]
        result.append(values)
    cur.close()
    if order_asc:
        result.reverse()
    return result


def get_by_id(id: int, def_value: Any = None, file: Optional[str] = None) -> Any:
    """
    get doc by id
    >>> clear(file=MEMORY_FILE)
    >>> insert_many( [{'name': 'A'}, {'name': 'B'}, {'name': 'C'}] )
    >>> get_by_id(1)['name']
    'A'
    >>> get_by_id(5, 'ne')
    'ne'
    """
    if file is not None:
        connect(file)
    if db is None:
        raise KudbError("please connect before using `get` method.")
    cur = db.cursor()
    cur.execute(SQLS["get_doc_by_id"], [id])
    data_one = cur.fetchone()
    if data_one is None:
        return def_value
    values, id = data_one
    values = json.loads(values)
    if isinstance(values, dict):
        values["id"] = id
    cur.close()
    return values


def get_by_tag(
    tag: str, limit: Optional[int] = None, file: Optional[str] = None
) -> List[Any]:
    """
    get doc by tag
    >>> clear(file=MEMORY_FILE)
    >>> insert_many( [{'name': 'A'}, {'name': 'B'}, {'name': 'C'}], tag_name='name' )
    >>> get_by_tag('B')[0]['name']
    'B'
    """
    if file is not None:
        connect(file)
    if db is None:
        raise KudbError("please connect before using `get` method.")
    if limit is None:
        limit = count_doc()
    result = []
    cur = db.cursor()
    for values, id in cur.execute(SQLS["get_doc_by_tag"], [tag, limit]):
        values = json.loads(values)
        if isinstance(values, dict):
            values["id"] = id
        result.append(values)
    cur.close()
    return result


def get(
    id: Optional[int] = None,
    key: Optional[str] = None,
    tag: Optional[str] = None,
    file: Optional[str] = None,
) -> Any:
    """
    get docs by id or key or tag
    >>> clear(file=MEMORY_FILE)
    >>> insert_many([{'name': 'A'},{'name': 'B'},{'name': 'C'}], tag_name='name')
    >>> get(id=1)['name']
    'A'
    >>> get(tag='C')[0]['name']
    'C'
    """
    if file is not None:
        connect(file)
    if db is None:
        raise KudbError("please connect before using `get` method.")
    if id is not None:
        return get_by_id(id)
    if tag is not None:
        return get_by_tag(tag)
    if key is not None:
        return get_key(key, None)
    raise KudbError("need id or key in `get` method")


def get_one(
    id: Optional[int] = None, tag: Optional[str] = None, file: Optional[str] = None
) -> Any:
    """
    get one doc by id or tag
    >>> clear(file=MEMORY_FILE)
    >>> insert_many([{'tag': 'A', 'v': 1}, {'tag': 'A', 'v': 2}, {'tag': 'B', 'v': 3}], tag_name='tag')
    >>> get_one(tag='A')['v']
    1
    """
    if file is not None:
        connect(file)
    if id is not None:
        return get(id)
    if tag is not None:
        r = get_by_tag(tag)
        if len(r) == 0:
            return None
        return r[0]
    raise KudbError("need id or tag in `get_one` method")


def insert(
    value: Any,
    file: Optional[str] = None,
    tag_name: Optional[str] = None,
    tag: Optional[str] = None,
) -> Optional[int]:
    """
    insert doc
    >>> clear(file=MEMORY_FILE)
    >>> insert({'name':'A'})
    1
    >>> insert({'name':'B'})
    2
    >>> [a['name'] for a in get_all()]
    ['A', 'B']

    insert doc with tag
    >>> clear()
    >>> insert({'name':'banana', 'price': 30}, tag='banana')
    1
    >>> get_by_tag("banana")[0]['price']
    30
    """
    if file is not None:
        connect(file)
    if db is None:
        raise KudbError("please connect before using `insert` method.")
    try:
        lastid = None
        cur = db.cursor()
        # check tag
        if tag is None:
            if tag_name is None:
                tag_name = get_tag_name()
            if isinstance(value, dict):
                if tag_name in value:
                    tag = value[tag_name]
        # auto detect tag_name
        if tag is None:
            if isinstance(value, dict):
                tag_name = list(value.keys())[0]
                set_tag_name(tag_name)
                tag = str(value[tag_name])
            else:
                tag = ""
        cur.execute(
            SQLS["insert_doc"],
            [
                json.dumps(value, ensure_ascii=False),
                tag,
                int(time.time()),
                int(time.time()),
            ],
        )
        lastid = cur.lastrowid
        cur.close()
        db.commit()
        return lastid
    except Exception as err:
        raise KudbError("database insert error:" + str(err)) from err


def insert_many(
    value_list: List[Any],
    file: Optional[str] = None,
    tag_name: Optional[str] = None,
    tag: Optional[str] = None,
) -> None:
    """
    insert many doc
    tag: all documents will have the same tag value
    tag_name: extract tag value from each document's key
    >>> clear(file=MEMORY_FILE)
    >>> insert_many([1,2,3,4,5])
    >>> get_by_id(1)
    1
    >>> get_by_id(2)
    2
    """
    if file is not None:
        connect(file)
    if db is None:
        raise KudbError("please connect before using `insert_many` method.")
    if not isinstance(value_list, list):
        raise KudbError("please set the list type arguments to `insert_many` method.")
    # make many values
    t = int(time.time())
    # check tag
    if tag is None:
        if tag_name is None:
            tag_name = get_tag_name()
        else:
            set_tag_name(tag_name)
    rows = []
    for val in value_list:
        tag_value = ""
        if tag is not None:
            # use tag argument for all documents
            tag_value = tag
        elif isinstance(val, dict):
            if tag_name in val:
                tag_value = val[tag_name]
        rows.append([json.dumps(val, ensure_ascii=False), tag_value, t, t])
    # insert
    try:
        cur = db.cursor()
        cur.executemany(SQLS["insert_doc"], rows)
        cur.close()
        db.commit()
    except Exception as err:
        raise KudbError("database insert error:" + str(err)) from err


def update(
    id: Optional[int] = None, new_value: Any = None, tag: Optional[str] = None
) -> None:
    """
    update doc

    update by id
    >>> clear(file=MEMORY_FILE)
    >>> insert_many([1,2,3,4,5])
    >>> get_by_id(1)
    1
    >>> update(1, 100)
    >>> get_by_id(1)
    100

    update by id:
    >>> clear()
    >>> insert_many([{"name": "A", "age": 30}, {"name": "B", "age": 20}], tag_name="name")
    >>> update(id=2, new_value={"name":"B", "age": 10})
    >>> get_by_tag("B")[0]["age"]
    10

    update by tag:
    >>> clear()
    >>> insert_many([{"name": "A", "age": 30}, {"name": "B", "age": 20}], tag_name="name")
    >>> update(tag="B", new_value={"name":"B", "age": 15})
    >>> get_by_tag("B")[0]["age"]
    15

    """
    if db is None:
        raise KudbError("please connect before using `update_doc` method.")
    # check tag
    if tag is None:
        tag_name = get_key("_tag", "tag")
        tag_value = ""
        if isinstance(new_value, dict):
            if tag_name in new_value:
                tag_value = str(new_value[tag_name])
    else:
        tag_name = "tag"
        tag_value = tag
    # update
    try:
        cur = db.cursor()
        sql = ""
        if id is not None:
            sql = SQLS["update_doc"]
            cur.execute(
                sql,
                [
                    json.dumps(new_value, ensure_ascii=False),
                    tag_value,
                    int(time.time()),
                    id,
                ],
            )
        elif tag is not None:
            sql = SQLS["update_doc_by_tag"]
            cur.execute(
                sql,
                [
                    json.dumps(new_value, ensure_ascii=False),
                    tag_value,
                    int(time.time()),
                    tag,
                ],
            )
        cur.close()
        db.commit()
    except Exception as err:
        raise KudbError("database update error:" + str(err)) from err


def update_by_tag(tag: str, new_value: Any) -> None:
    """
    update doc value by tag
    >>> clear()
    >>> insert_many([{"name": "A", "age": 30}, {"name": "B", "age": 20}], tag_name="name")
    >>> update_by_tag("B", {"name":"B", "age": 15})
    >>> get_by_tag("B")[0]["age"]
    15
    """
    update(tag=tag, new_value=new_value)


def update_by_id(id: int, new_value: Any) -> None:
    """
    update doc value by tag
    >>> clear()
    >>> insert_many([{"name": "A", "age": 30}, {"name": "B", "age": 20}], tag_name="name")
    >>> update_by_tag("B", {"name":"B", "age": 15})
    >>> get_by_tag("B")[0]["age"]
    15
    """
    update(id=id, new_value=new_value)


def delete(
    id: Optional[int] = None,
    key: Optional[str] = None,
    tag: Optional[str] = None,
    doc_keys: Optional[Dict[str, Any]] = None,
    file: Optional[str] = None,
) -> None:
    """
    delete by id or key
    >>> clear(file=MEMORY_FILE)
    >>> insert_many([1,2,3])
    >>> delete(id=3)
    >>> [a for a in get_all()]
    [1, 2]

    delete key in key-value store:
    >>> clear()
    >>> set_key('Taro', 30)
    >>> set_key('Jiro', 18)
    >>> delete(key='Taro')
    >>> list(get_keys())
    ['Jiro']

    delete doc_keys in docs
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
    """
    if file is not None:
        connect(file)
    if db is None:
        raise KudbError("please connect before using `delete` method.")
    if id is not None:
        cur = db.cursor()
        cur.execute(SQLS["delete_doc"], [id])
        cur.close()
        db.commit()
        return
    if tag is not None:
        cur = db.cursor()
        cur.execute(SQLS["delete_doc_by_tag"], [tag])
        cur.close()
        db.commit()
        return
    if key is not None:
        delete_key(key)
        return
    if doc_keys is not None:
        docs = find(keys=doc_keys)
        for row in docs:
            id = row["id"]
            delete(id=id)
        return
    raise KudbError("should set id or key in `delete` method")


def clear_doc(file: Optional[str] = None) -> None:
    """
    clear all doc

    >>> clear(file=MEMORY_FILE)
    >>> insert_many([1,2,3,4,5])
    >>> count_doc()
    5
    >>> clear_doc()
    >>> count_doc()
    0
    """
    if file is not None:
        connect(file)
    if db is None:
        raise KudbError("please connect before using `clear_doc` method.")
    cur = db.cursor()
    cur.execute(SQLS["clear_doc"], [])
    cur.close()
    db.commit()


def clear(file: Optional[str] = None) -> None:
    """
    clear doc and key-value-store

    >>> clear(file=MEMORY_FILE)
    >>> insert_many([1,2,3,4,5])
    >>> count_doc()
    5
    >>> clear_doc()
    >>> count_doc()
    0
    """
    if file is not None:
        connect(file)
    clear_keys()
    clear_doc()


def find(
    callback: Optional[Callable[[Any], bool]] = None,
    keys: Optional[Dict[str, Any]] = None,
    limit: Optional[int] = None,
) -> List[Any]:
    """
    find doc by lambda
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
    """
    if db is None:
        raise KudbError("please connect before using `find` method.")
    result = []
    cur = db.cursor()
    # callback
    if (callback is None) and (keys is not None):
        callback = lambda values: (
            True
            if sum([(0 if (values[k] == v) else 1) for k, v in keys.items()]) == 0
            else False
        )
    # find
    for row in cur.execute(SQLS["select_doc"]):
        values = json.loads(row[0])
        if isinstance(values, dict):
            values["id"] = row[1]
        if callback is not None and callback(values):
            result.append(values)
            if (limit is not None) and (len(result) >= limit):
                break
    cur.close()
    return result


def find_one(
    callback: Optional[Callable[[Any], bool]] = None,
    keys: Optional[Dict[str, Any]] = None,
    limit: Optional[int] = None,
) -> Any:
    """
    find one doc by lambda
    >> clear(file=MEMORY_FILE)
    >> insert_many([{'name': 'Taro', 'age': 30}, {'name': 'Jiro', 'age': 18}])
    >> find_one(keys={'name': 'Jiro'})['age']
    18
    """
    r = find(callback=callback, keys=keys, limit=limit)
    if len(r) == 0:
        return None
    return r[0]


def set_tag_name(tag_name: str) -> None:
    """set tag name"""
    set_key("_tag", tag_name)


def get_tag_name(def_tag_name: str = "tag") -> Any:
    """get tag name"""
    return get_key("_tag", def_tag_name)


def get_high_score(limit: int = 10, score_key: str = "score") -> List[Any]:
    """
    get high score docs
    >>> clear(file=MEMORY_FILE)
    >>> insert_many([{'name': 'A', 'score': 50}, {'name': 'B', 'score': 80}, {'name': 'C', 'score': 70}])
    >>> [a['name'] for a in get_high_score(2)]
    ['B', 'C']
    """
    result = get_all()
    result.sort(key=lambda x: x.get(score_key, 0), reverse=True)
    return result[:limit]


def insert_score(
    score: int,
    name: str,
    meta: Optional[Dict[str, Any]] = None,
    score_key: str = "score",
    file: Optional[str] = None,
) -> Optional[int]:
    """
    insert score doc
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
    """
    if meta is None:
        meta = {}
    meta["name"] = name
    meta[score_key] = score
    return insert(meta, file=file)


# 公開APIを定義
__all__ = [
    # Constants
    "MEMORY_FILE",
    "SQLITE_MAX_INT",
    # Connection
    "connect",
    "change_db",
    "close",
    # KVS functions
    "get_key",
    "set_key",
    "set_keys_from_dict",
    "delete_key",
    "get_keys",
    "get_info",
    "kvs_json",
    "clear_keys",
    # Document functions
    "count_doc",
    "get_all",
    "recent",
    "get_by_id",
    "get_by_tag",
    "get",
    "get_one",
    "insert",
    "insert_many",
    "update",
    "update_by_tag",
    "update_by_id",
    "delete",
    "clear_doc",
    "clear",
    "find",
    "find_one",
    "set_tag_name",
    "get_tag_name",
    # Score functions
    "get_high_score",
    "insert_score",
]

if __name__ == "__main__":
    import doctest

    doctest.testmod()
