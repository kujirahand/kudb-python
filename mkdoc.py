"""
mkdoc.py
"""
import re
import kudb

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

# check doc
def check_doc(doc):
    res = []
    last_s = ''
    code_list = []
    for line in (doc.strip() + '\n').split('\n'):
        s = line.strip()
        if (last_s.startswith('>>>')) or (s.startswith('>>>')):
            code_list.append(s)
        else:
            print('@ len=', len(code_list))
            if len(code_list) > 0:
                src2 = "\n".join(code_list)
                res.append('```\n' + src2 + '\n```\n')
                # print('code:', src2)
                code_list = []
            res.append(s)
        last_s = s
        # print('+len=', len(code_list))
    res[0] += "\n"
    return "\n".join(res)

text = '# kudb functions\n\n'
for name in dir(kudb):
    if re.match('^__', name):
        # print('skip:', name)
        continue
    if name not in def_list:
        continue
    text += '## ' + def_list[name] + '\n\n'
    f = eval(f'kudb.%s' % name)
    # text += f.__builtins__ + '\n'
    text += check_doc(f.__doc__) + '\n\n'

print(text)
with open('./docs/functions.md', 'w', encoding='utf-8') as fp:
    fp.write(text)
