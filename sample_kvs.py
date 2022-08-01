import kudb as kvs
import json

kvs.connect()
kvs.set_key('hoge', 1234)
kvs.set_key('fuga', 'いろは')
kvs.set_key('foo', [1,2,3])

# get
print(kvs.get(key='fuga'))

print(kvs.get_keys())
kvs.delete('fuga')
print(kvs.get_keys())

# enums
for key in kvs.get_keys():
    print(key, '=', json.dumps(kvs.get(key=key), ensure_ascii=False))

# get_info
print('info=', kvs.get_info('hoge'))

print(kvs.kvs_json())
kvs.close()
