import kudb
kudb.connect('test.db')
kudb.clear()

# データの挿入
kudb.insert_many([
    {"name": "A", "age": 10},
    {"name": "B", "age": 11},
    {"name": "C", "age": 12},
    {"name": "D", "age": 13},
    {"name": "E", "age": 14}], tag_name='name')

# Eを削除(idを指定)
kudb.delete(id=5)

# Cを削除(tagを指定)
kudb.delete(tag='C')

# データの更新(idを指定)
kudb.update_by_id(1, {'name': 'A', 'age': 22})
print('update.A=22 >', kudb.get(id=1))

# データの更新(tagを指定)
kudb.update_by_tag('B', {'name': 'B', 'age': 23})
print('update.B=23 >', kudb.get(tag='B'))

