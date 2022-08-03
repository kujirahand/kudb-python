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
# pylint: disable=C0103,C301,W0622,W0603
import sqlite3
import time
import json

db = None
cache_db = {}
CACHE_KEYS = {}
SQLS = {}
MEMORY_FILE = ':memory:'
cur_filename = MEMORY_FILE
SQLITE_MAX_INT=9223372036854775807
# SQL template
SQLS_TEMPLATE = {
    # kvs
    'create': '''
    CREATE TABLE IF NOT EXISTS __TABLE_NAME__ (
        key_id INTEGER PRIMARY KEY,
        key TEXT UNIQUE,
        value TEXT DEFAULT '',
        ctime INTEGER DEFAULT 0,
        mtime INTEGER DEFAULT 0
    )
    ''',
    'select': 'SELECT value FROM __TABLE_NAME__ WHERE key=?',
    'select_info': 'SELECT * FROM __TABLE_NAME__ WHERE key=?',
    'keys': 'SELECT key FROM __TABLE_NAME__',
    'insert': 'INSERT INTO __TABLE_NAME__ (key, value, ctime, mtime) VALUES (?, ?, ?, ?)',
    'update': 'UPDATE __TABLE_NAME__ SET value=?, mtime=? WHERE key=?',
    'delete': 'DELETE FROM __TABLE_NAME__ WHERE key=?',
    'clear': 'DELETE FROM __TABLE_NAME__',
    # doc
    'create_doc': '''
    CREATE TABLE IF NOT EXISTS doc__TABLE_NAME__ (
        id INTEGER PRIMARY KEY,
        value TEXT DEFAULT '',
        ctime INTEGER DEFAULT 0,
        mtime INTEGER DEFAULT 0
    )
    ''',
    'select_doc': 'SELECT value, id FROM doc__TABLE_NAME__',
    'select_doc_desc': 'SELECT value, id FROM doc__TABLE_NAME__ WHERE id <= ? ORDER BY id DESC LIMIT ?',
    'select_doc_asc': 'SELECT value, id FROM doc__TABLE_NAME__ WHERE id >= ? ORDER BY id ASC LIMIT ?',
    'recent_doc': 'SELECT value, id FROM doc__TABLE_NAME__ ORDER BY id DESC LIMIT ? OFFSET ?',
    'get_doc_by_id': 'SELECT value, id FROM doc__TABLE_NAME__ WHERE id=?',
    'insert_doc': 'INSERT INTO doc__TABLE_NAME__ (value, ctime, mtime) VALUES (?, ?, ?)',
    'update_doc': 'UPDATE doc__TABLE_NAME__ SET value=?, mtime=? WHERE id=?',
    'delete_doc': 'DELETE FROM doc__TABLE_NAME__ WHERE id=?',
    'clear_doc': 'DELETE FROM doc__TABLE_NAME__',
    'count_doc': 'SELECT count(id) FROM doc__TABLE_NAME__',
}

def connect(filename = ':memory:', table_name='kudb'):
    """Connect to database"""
    global SQLS, cur_filename, db
    # generate sqls
    SQLS = {}
    for key, val in SQLS_TEMPLATE.items():
        SQLS[key] = val.replace('__TABLE_NAME__', table_name)
    # check cache
    if filename in cache_db: # already open?
        db = cache_db[filename] # use_cache
        cur_filename = filename
        return db
    # connect to sqlite3
    db = sqlite3.connect(filename, check_same_thread=False)
    cache_db[filename] = db
    cur_filename = filename
    try:
        # create table
        db.executescript(SQLS['create'] + ';' + SQLS['create_doc'])
        # make cache keys
        get_keys(True)
        return db
    except Exception as err:
        raise Exception('could not initalize database file: ' + str(err)) from err

def change_db(filename = ':memory:', table_name = 'kudb'):
    """Change Database"""
    connect(filename, table_name)

def close():
    """close database"""
    global db, cur_filename
    if db is not None:
        db.close()
        del cache_db[cur_filename]
    db = None
    cur_filename = ''

def get_key(key, default = '', file=None):
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
        raise Exception('please connect before using `get` method.')
    if key not in CACHE_KEYS:
        return default
    cur = db.cursor()
    try:
        cur.execute(SQLS['select'], [key])
        values = cur.fetchone()
        return json.loads(values[0])
    except Exception as err:
        raise Exception('could not read database: ' + str(err)) from err
    finally:
        cur.close()

def get_info(key, default = ''):
    """get data and info"""
    if db is None:
        raise Exception('please connect before using `get` method.')
    if key not in CACHE_KEYS:
        return default
    try:
        cur = db.cursor()
        cur.execute(SQLS['select_info'], [key])
        values = cur.fetchone()
        return values
    except Exception as err:
        raise Exception('could not read database: ' + str(err)) from err
    finally:
        cur.close()

def set_key(key, value, file=None):
    """
    set data by key
    >>> set_key('hoge', 30, file=':memory:')
    >>> get_key('hoge')
    30
    >>> set_key(1, 40)
    >>> get_key(1)
    40
    """
    if file is not None:
        connect(file)
    if db is None:
        raise Exception('please connect before using `set_key` method.')
    try:
        cur = db.cursor()
        if key in CACHE_KEYS:
            cur.execute(SQLS['update'], [value, int(time.time()), key])
        else:
            cur.execute(
                SQLS['insert'],
                [
                    key,
                    json.dumps(value, ensure_ascii=False),
                    int(time.time()),
                    int(time.time())
                ]
            )
            CACHE_KEYS[key] = True
        cur.close()
        db.commit()
    except Exception as err:
        raise Exception('database could not write key: ' + str(err)) from err

def delete_key(key):
    """delete key"""
    if db is None:
        raise Exception('please connect before using `delete_key` method.')
    try:
        cur = db.cursor()
        if key in CACHE_KEYS:
            cur.execute(SQLS['delete'], [key])
            del CACHE_KEYS[key]
        cur.close()
        db.commit()
    except Exception as err:
        raise Exception('database could not delete key: ' + str(err)) from err

def get_keys(clear_cache = True):
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
        cur.execute(SQLS['keys'])
        CACHE_KEYS = {}
        for i in cur.fetchall():
            CACHE_KEYS[i[0]] = True
    return CACHE_KEYS.keys()

def kvs_json():
    """dump key-value items to json"""
    obj = {}
    for key in get_keys():
        obj[key] = get_key(key)
    return json.dumps(obj, ensure_ascii=False)

def clear_keys():
    """clear all keys"""
    global CACHE_KEYS
    if db is None:
        raise Exception('please connect before using `clear_keys` method.')
    try:
        cur = db.cursor()
        cur.execute(SQLS['clear'])
        CACHE_KEYS = {}
        cur.close()
        db.commit()
    except Exception as err:
        raise Exception('could not read database: ' + str(err)) from err

def count_doc(file=None):
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
        raise Exception('please connect before using `count_doc` method.')
    try:
        cur = db.cursor()
        cur.execute(SQLS['count_doc'])
        val = cur.fetchone()
        return val[0]
    except Exception as err:
        raise Exception('could not count docs:' + str(err)) from err

def get_all(limit=None, order_asc=True, from_id=None, file=None):
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
        raise Exception('please connect before using `get_all` method.')
    if limit is None:
        limit = count_doc()
    sql = SQLS['select_doc_asc']
    if order_asc:
        if from_id is None:
            from_id = 1
    else:
        sql =  SQLS['select_doc_desc']
        if from_id is None:
            from_id = SQLITE_MAX_INT
    # select doc
    result = []
    cur = db.cursor()
    for row in cur.execute(sql, [from_id, limit]):
        values = json.loads(row[0])
        if isinstance(values, dict):
            values['id'] = row[1]
        result.append(values)
    cur.close()
    return result

def recent(limit=100, offset=0):
    """
    get recent docs
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
    """
    if db is None:
        raise Exception('please connect before using `recent` method.')
    cur = db.cursor()
    result = []
    for row in cur.execute(SQLS['recent_doc'], [limit, offset]):
        values = json.loads(row[0])
        if isinstance(values, dict):
            values['id'] = row[1]
        result.append(values)
    cur.close()
    return result

def get_by_id(id, def_value=None, file=None):
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
        raise Exception('please connect before using `get` method.')
    cur = db.cursor()
    cur.execute(SQLS['get_doc_by_id'], [id])
    data_one = cur.fetchone()
    if data_one is None:
        return def_value
    values, id = data_one
    values = json.loads(values)
    if isinstance(values, dict):
        values['id'] = id
    cur.close()
    return values

def get(id=None, key=None, file=None):
    """
    get doc by id or key
    >>> clear(file=MEMORY_FILE)
    >>> insert_many([{'name': 'A'},{'name': 'B'},{'name': 'C'}])
    >>> get(id=1)['name']
    'A'
    """
    if file is not None:
        connect(file)
    if db is None:
        raise Exception('please connect before using `get` method.')
    if id is not None:
        return get_by_id(id)
    if key is not None:
        return get_key(key, None)
    raise Exception('need id or key in `get` method')

def insert(values, file=None):
    """
    insert doc
    >>> clear(file=MEMORY_FILE)
    >>> insert({'name':'A'})
    1
    >>> insert({'name':'B'})
    2
    >>> [a['name'] for a in get_all()]
    ['A', 'B']
    """
    if file is not None:
        connect(file)
    if db is None:
        raise Exception('please connect before using `insert` method.')
    try:
        lastid = None
        cur = db.cursor()
        cur.execute(SQLS['insert_doc'], [json.dumps(values), int(time.time()), int(time.time())])
        lastid = cur.lastrowid
        cur.close()
        db.commit()
        return lastid
    except Exception as err:
        raise Exception('database insert error:' + str(err)) from err

def insert_many(value_list, file=None):
    """
    insert many doc
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
        raise Exception('please connect before using `insert_many` method.')
    if not isinstance(value_list, list):
        raise Exception('please set the list type arguments to `insert_many` method.')
    # make many values
    t = int(time.time())
    rows = []
    for val in value_list:
        rows.append([json.dumps(val), t, t])
    # insert
    try:
        cur = db.cursor()
        cur.executemany(SQLS['insert_doc'], rows)
        cur.close()
        db.commit()
    except Exception as err:
        raise Exception('database insert error:' + str(err)) from err

def update(doc_id, values):
    """
    update doc
    >>> clear(file=MEMORY_FILE)
    >>> insert_many([1,2,3,4,5])
    >>> get_by_id(1)
    1
    >>> update(1, 100)
    >>> get_by_id(1)
    100
    """
    if db is None:
        raise Exception('please connect before using `update_doc` method.')
    try:
        cur = db.cursor()
        cur.execute(SQLS['update_doc'], [json.dumps(values), int(time.time()), doc_id])
        cur.close()
        db.commit()
    except Exception as err:
        raise Exception('database update error:' + str(err)) from err

def delete(id=None, key=None, file=None):
    """
    delete by id or key
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
    """
    if file is not None:
        connect(file)
    if db is None:
        raise Exception('please connect before using `delete` method.')
    if id is not None:
        cur = db.cursor()
        cur.execute(SQLS['delete_doc'], [id])
        cur.close()
        db.commit()
        return
    if key is not None:
        delete_key(key)
        return
    raise Exception('should set id or key in `delete` method')

def clear_doc(file=None):
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
        raise Exception('please connect before using `clear_doc` method.')
    cur = db.cursor()
    cur.execute(SQLS['clear_doc'], [])
    cur.close()
    db.commit()

def clear(file=None):
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

def find(callback, limit=None):
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
    """
    if db is None:
        raise Exception('please connect before using `find` method.')
    result = []
    cur = db.cursor()
    for row in cur.execute(SQLS['select_doc']):
        values = json.loads(row[0])
        if isinstance(values, dict):
            values['id'] = row[1]
        if callback(values):
            result.append(values)
            if (limit is not None) and (len(result) >= limit):
                break
    cur.close()
    return result

if __name__ == '__main__':
    import doctest
    doctest.testmod()
