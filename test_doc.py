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
