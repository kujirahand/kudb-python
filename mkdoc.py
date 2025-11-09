"""
mkdoc.py
"""
import re
import kudb

# check 1st
with open('kudb/kudb.py', encoding='utf-8') as fp:
    src = fp.read()

# 関数定義を抽出(複数行対応)
def_list = {}
lines = src.split('\n')
i = 0
while i < len(lines):
    line = lines[i]
    # 関数定義を検出
    m = re.match(r'^def ([A-Za-z0-9_]+)', line)
    if m:
        name = m.group(1)
        print(name)
        # 関数定義を完全に取得(複数行対応)
        func_def = line
        # 閉じ括弧が見つかるまで次の行を追加
        if '(' in line and ')' not in line.split('->')[0]:
            i += 1
            while i < len(lines):
                func_def += ' ' + lines[i].strip()
                # 戻り値の前に閉じ括弧があるか、または行末に閉じ括弧があるかチェック
                if ')' in lines[i]:
                    break
                i += 1
        # def と末尾のコロンを削除
        def_list[name] = re.sub(r'(^def |:\s*$)', '', func_def).strip()
    i += 1

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
                res.append('```py\n' + src2 + '\n```\n')
                # print('code:', src2)
                code_list = []
            res.append(s)
        last_s = s
        # print('+len=', len(code_list))
    res[0] += "\n"
    return "\n".join(res)

print('\n=== Generating documentation ===')
text = '# kudb functions\n\n'
for name in dir(kudb):
    if re.match('^__', name):
        # print('skip:', name)
        continue
    if name not in def_list:
        continue
    text += '## ' + def_list[name] + '\n\n'
    f = getattr(kudb, name)
    # text += f.__builtins__ + '\n'
    if hasattr(f, '__doc__') and f.__doc__:
        text += check_doc(f.__doc__) + '\n\n'

print(text)
with open('./docs/functions.md', 'w', encoding='utf-8') as fp:
    fp.write(text)
