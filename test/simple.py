"""
kudb simple test
"""
# pylint: disable=C0413,W1309,C0103

import sys
import os
import json

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'kudb'))
sys.path.append(base_dir)
import kudb

# get and set
kudb.connect()
kudb.set_key('a', 1234)
assert 1234 == kudb.get(key='a'), 'get'
kudb.set_key('b', [1,2,3,4])
assert 4 == len(kudb.get(key='b')), 'get :: list'

# clear and delete and keys
kudb.clear()
kudb.set_key('c', 'abc')
kudb.set_key('d', 'cde')
kudb.delete(key='d')
assert json.dumps(list(kudb.get_keys())) == '["c"]', f'keys=%s' % json.dumps(list(kudb.get_keys()))
kudb.close()

# change table_name
kudb.connect(table_name='no1')
kudb.set_key('hello', 123)
assert 123 == kudb.get(key='hello'), 'get table_name=no1'

kudb.connect(table_name='no2')
assert '' == kudb.get_key('hello', ''), f'get hello=%s table_name=no2' % kudb.get_key('hello', '')
kudb.close()

# multi database
kudb.connect(':memory:')
kudb.set_key('hello', 1234)
kudb.connect('test.db')
assert '' == kudb.get_key('hello', ''), 'multidatabase'
kudb.close()
os.unlink('test.db')

# insert
kudb.connect(':memory:')
kudb.insert({'name': 'Tako', 'age': 20})
kudb.insert({'name': 'Ika', 'age': 17})
age_total = 0
for c in kudb.get_all():
    age_total += c['age']
assert 37 == age_total, 'insert error'
