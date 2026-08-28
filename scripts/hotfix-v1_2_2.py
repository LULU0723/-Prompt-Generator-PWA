from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old = "let roleLoadedIds = {A:null,B:null};\n"
new = "let roleLoadedIds = {A:null,B:null};\nlet generatorMode = 'full';\n"
if "let generatorMode = 'full';" not in s:
    if old not in s:
        raise SystemExit('generatorMode insertion anchor not found')
    s = s.replace(old, new, 1)

s = s.replace('V1.2.1 Quick Prompt', 'V1.2.2 Quick Prompt Hotfix')
s = s.replace('V1.2.1 Composer · Quick Prompt Mode', 'V1.2.2 Composer · Quick Prompt Mode')
p.write_text(s, encoding='utf-8')
print('V1.2.2 hotfix applied')
