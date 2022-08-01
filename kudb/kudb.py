"""
Simple document database Library
"""
# pylint: disable=C0103,W0622,W0603
import sqlite3
import time
import json

db = None
cache_db = {}
CACHE_KEYS = {}
sqls = {}
cur_filename = ':memory:'
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
    'recent_doc': 'SELECT value, id FROM doc__TABLE_NAME__ ORDER BY id DESC LIMIT ?',
    'get_doc_by_id': 'SELECT value, id FROM doc__TABLE_NAME__ WHERE id=?',
    'insert_doc': 'INSERT INTO doc__TABLE_NAME__ (value, ctime, mtime) VALUES (?, ?, ?)',
    'update_doc': 'UPDATE doc__TABLE_NAME__ SET value=?, mtime=? WHERE id=?',
    'delete_doc': 'DELETE FROM doc__TABLE_NAME__ WHERE id=?',
    'clear_doc': 'DELETE FROM doc__TABLE_NAME__',
}

def connect(filename = ':memory:', table_name='kudb'):
    """Connect to database"""
    global sqls, cur_filename
    # generate sqls
    sqls = {}
    for key in SQLS_TEMPLATE.keys():
        sqls[key] = SQLS_TEMPLATE[key].replace('__TABLE_NAME__', table_name)
    # connect to sqlite3
    global db
    if filename in cache_db: # already open?
        db = cache_db[filename] # use_cache
    else:
        db = sqlite3.connect(filename)
        cache_db[filename] = db
    cur_filename = filename
    try:
        # create table
        cur = db.cursor()
        cur.execute(sqls['create'], [])
        cur.execute(sqls['create_doc'], [])
        # make cache keys
        get_keys(True)
    except Exception as err:
        raise Exception('could not initalize database file: ' + str(err)) from err
    finally:
        cur.close()
    return db

def change_db(filename = ':memory:', table_name = 'kudb'):
    """Change Database"""
    connect(filename, table_name)

def close():
    """close database"""
    global db, cur_filename
    if db is not None:
        del cache_db[cur_filename]
        db.close()
    db = None
    cur_filename = ''

def get_key(key, default = ''):
    """get data by key"""
    if db is None:
        raise Exception('please connect before using `get` method.')
    if key not in CACHE_KEYS:
        return default
    try:
        cur = db.cursor()
        cur.execute(sqls['select'], [key])
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
        cur.execute(sqls['select_info'], [key])
        values = cur.fetchone()
        return values
    except Exception as err:
        raise Exception('could not read database: ' + str(err)) from err
    finally:
        cur.close()

def set_key(key, value):
    """set data by key"""
    if db is None:
        raise Exception('please connect before using `set_key` method.')
    try:
        cur = db.cursor()
        if key in CACHE_KEYS:
            cur.execute(sqls['update'], [value, int(time.time()), key])
        else:
            cur.execute(
                sqls['insert'],
                [
                    key,
                    json.dumps(value, ensure_ascii=False),
                    int(time.time()),
                    int(time.time())
                ]
            )
            CACHE_KEYS[key] = True
    except Exception as err:
        raise Exception('could not read database: ' + str(err)) from err
    finally:
        cur.close()

def delete_key(key):
    """delete key"""
    if db is None:
        raise Exception('please connect before using `delete_key` method.')
    try:
        cur = db.cursor()
        if key in CACHE_KEYS:
            cur.execute(sqls['delete'], [key])
            del CACHE_KEYS[key]
    except Exception as err:
        raise Exception('could not read database: ' + str(err)) from err
    finally:
        cur.close()

def get_keys(clear_cache = True):
    """get keys"""
    global CACHE_KEYS
    if db is None:
        return []
    # Use Cache?
    if clear_cache or len(CACHE_KEYS) == 0:
        cur = db.cursor()
        cur.execute(sqls['keys'])
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
        cur.execute(sqls['clear'])
        CACHE_KEYS = {}
    except Exception as err:
        raise Exception('could not read database: ' + str(err)) from err
    finally:
        cur.close()

def get_all():
    """get all doc"""
    if db is None:
        raise Exception('please connect before using `all` method.')
    result = []
    cur = db.cursor()
    for row in cur.execute(sqls['select_doc']):
        values = json.loads(row[0])
        values['id'] = row[1]
        result.append(values)
    cur.close()
    return result

def recent(limit):
    """get recent docs"""
    if db is None:
        raise Exception('please connect before using `recent` method.')
    cur = db.cursor()
    result = []
    for row in cur.execute(sqls['recent_doc'], [limit]):
        values = json.loads(row[0])
        values['id'] = row[1]
        result.append(values)
    cur.close()
    return result

def get_by_id(id):
    """get doc by id"""
    if db is None:
        raise Exception('please connect before using `get` method.')
    cur = db.cursor()
    cur.execute(sqls['get_doc_by_id'], [id])
    data_one = cur.fetchone()
    if data_one is None:
        return None
    values, id = data_one
    values = json.loads(values)
    values['id'] = id
    cur.close()
    return values

def get(id=None, key=None, file=None):
    """get doc by id or key"""
    if file is not None:
        connect(file)
    if db is None:
        raise Exception('please connect before using `get` method.')
    if id is not None:
        return get_by_id(id)
    if key is not None:
        return get_key(key, None)
    raise Exception('need id or key in `get` method')

def insert(values):
    """insert doc"""
    if db is None:
        raise Exception('please connect before using `insert` method.')
    cur = db.cursor()
    cur.execute(sqls['insert_doc'], [json.dumps(values), int(time.time()), int(time.time())])
    cur.close()
    return cur.lastrowid

def update(doc_id, values):
    """update doc"""
    if db is None:
        raise Exception('please connect before using `update_doc` method.')
    cur = db.cursor()
    cur.execute(sqls['update_doc'], [json.dumps(values), int(time.time()), doc_id])
    cur.close()
    return doc_id

def delete(id=None, key=None):
    """delete by id or key"""
    if db is None:
        raise Exception('please connect before using `delete_doc` method.')
    if id is not None:
        cur = db.cursor()
        cur.execute(sqls['delete_doc'], [id])
        cur.close()
        return
    if key is not None:
        delete_key(key)
        return
    raise Exception('should set id or key in `delete` method')

def clear_doc():
    """clear all"""
    if db is None:
        raise Exception('please connect before using `clear_doc` method.')
    cur = db.cursor()
    cur.execute(sqls['clear_doc'], [])
    cur.close()

def clear():
    """clear all"""
    clear_keys()
    clear_doc()

def find(callback):
    """find doc by lambda"""
    if db is None:
        raise Exception('please connect before using `find` method.')
    result = []
    cur = db.cursor()
    for row in cur.execute(sqls['select_doc']):
        values = json.loads(row[0])
        values['id'] = row[1]
        if callback(values):
            result.append(values)
    cur.close()
    return result
# end of kudb
