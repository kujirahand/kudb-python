"""
kudb simple test
"""
# pylint: disable=C0413,W1309,C0103

import sys
import os
import json
import kudb

# insert
kudb.connect(':memory:')
kudb.insert({'name': 'Tako', 'age': 20})
kudb.insert({'name': 'Ika', 'age': 17})
age_total = 0
for c in kudb.get_all():
    age_total += c['age']
assert 37 == age_total, 'insert error'
kudb.close()

# test
kudb.connect()
kudb.insert(100)
assert 100 == kudb.get_by_id(1), 'insert value 100'

# clear ------------------------
kudb.clear()
assert 0 == kudb.count_doc(), 'clear'

# insert with tag
kudb.insert({'name': 'Tako', 'age': 18}, tag_name='name')
kudb.insert({'name': 'Ika', 'age': 19})
# insert_many with tag
kudb.insert_many([{'name': 'Poko', 'age': 12}, {'name': 'Foo', 'age': 13}], tag_name='name')

# delete id=2
kudb.delete(id=2)
assert kudb.get(id=2) is None, 'delete by id'

# deleta tag=Foo
kudb.delete(tag='Foo')
assert len(kudb.get(tag='Foo')) == 0, 'delete by tag'

# update by id
kudb.update_by_id(1, {'name': 'Tako', 'age': 22})
assert kudb.get(id=1)['age'] == 22, 'update by id'

# update by tag
kudb.update_by_tag('Tako', new_value={'name': 'Tako', 'age': 23})
assert kudb.get(tag='Tako')[0]['age'] == 23, 'update doc by tag 1'

kudb.update(tag='Tako', new_value={'name': 'Tako', 'age': 19})
assert kudb.get(tag='Tako')[0]['age'] == 19, 'update doc by tag 2'

# get_one
kudb.clear()
kudb.insert({'name': 'Taro', 'age': 30}, tag='Taro')
kudb.insert({'name': 'Jiro', 'age': 29}, tag='Jiro')
kudb.insert({'name': 'Sabu', 'age': 28}, tag='Sabu')
assert kudb.get_one(tag='Taro')['name'] == 'Taro', 'get_one'
assert kudb.get_one(tag='Goro') is None, 'get_one (None)'


