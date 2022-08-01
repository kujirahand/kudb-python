import kudb
import re

# check 1st
with open('kudb/kudb.py', encoding='utf-8') as fp:
    src = fp.read()
def_list = {}
for line in src.split('\n'):
    m = re.match(r'^def ([A-Za-z0-9_]+)', line)
    if not m:
        continue
    name = m.group(1)
    print(name)
    def_list[name] = re.sub(r'(^def |:$)', '', line)
print(def_list)

# check doc
def chk(doc):
    res = []
    last = ''
    for s in doc.strip().split('\n'):
        s = s.strip()
        if last.startswith('>>>') or s.startswith('>>>'):
            res.append(' ' + s)
        else:
            res.append(s)
        last = s
    res[0] += "\n"
    return "\n".join(res)

text = '# kudb module functions\n\n'
for name in dir(kudb):
    if re.match('^__', name):
        # print('skip:', name)
        continue
    if name not in def_list:
        continue
    text += '## ' + def_list[name] + '\n\n'
    f = eval(f'kudb.%s' % name)
    # text += f.__builtins__ + '\n'
    text += chk(f.__doc__) + '\n\n'

print(text)
with open('./docs/functions.md', 'w', encoding='utf-8') as fp:
    fp.write(text)
