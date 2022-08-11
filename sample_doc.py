import kudb
import json

kudb.connect()
kudb.insert({'name': 'Taro', 'age': 10})
kudb.insert({'name': 'Ika', 'age': 11})
kudb.insert({'name': 'Poko', 'age': 12})
kudb.insert({'name': 'Foo', 'age': 13})

print("===")
for c in kudb.get_all():
    print(c)

print("===")
for c in kudb.recent(2):
    print(c)

print("===")
print('id=1', kudb.get(id=1))

print("===")
print(json.dumps(kudb.find(lambda v: v['name']=='Ika')))
print(json.dumps(kudb.find(keys={"name": "Ika"})))
print(json.dumps(kudb.find(keys={"age": 11})))
print("===")
kudb.clear()
a = kudb.get_all()
print('len=', len(a))

