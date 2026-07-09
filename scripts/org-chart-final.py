#!/usr/bin/env python3
"""Build 4R Labs org chart - final version."""

W = 82

def empty_row():
    return [' '] * W

def insert_str(row, col, s):
    for i, ch in enumerate(s):
        row[col + i] = ch

def make_outer():
    r = empty_row(); r[0] = '╔'
    for i in range(1, W-1): r[i] = '═'
    r[W-1] = '╗'; return r

def make_sep():
    r = empty_row(); r[0] = '╠'
    for i in range(1, W-1): r[i] = '═'
    r[W-1] = '╣'; return r

def make_bottom():
    r = empty_row(); r[0] = '╚'
    for i in range(1, W-1): r[i] = '═'
    r[W-1] = '╝'; return r

def make_content(content=''):
    r = empty_row(); r[0] = '║'; r[W-1] = '║'
    if content:
        insert_str(r, (W - 2 - len(content)) // 2 + 1, content)
    return r

def make_box(lines, width):
    top = ['╔'] + ['═'] * (width - 2) + ['╗']
    bottom = ['╚'] + ['═'] * (width - 2) + ['╝']
    result = [top]
    for text in lines:
        iw = width - 2
        padded = text.center(iw) if len(text) < iw else text[:iw]
        result.append(['║'] + list(padded) + ['║'])
    result.append(bottom)
    return result

L = []

L.append(make_outer())
L.append(make_content('4R LABS'))
L.append(make_content('ORG CHART — RLA'))
L.append(make_sep())
L.append(make_content())

# CEO
ceo_w, ceo_s, ceo_c = 25, 29, 41
for bl in make_box(['OpenClaw  (CEO)', '● paused'], ceo_w):
    r = empty_row(); r[0] = '║'; r[W-1] = '║'
    insert_str(r, ceo_s, ''.join(bl)); L.append(r)

r = empty_row(); r[0] = '║'; r[W-1] = '║'; r[ceo_c] = '│'
L.append(r)

# Branch L2
esp_w, esp_s, esp_c = 33, 1, 17
cto_w, cto_s, cto_c = 25, 51, 63

r = empty_row(); r[0] = '║'; r[W-1] = '║'
r[esp_c] = '╔'
for c in range(esp_c+1, cto_c): r[c] = '═'
r[cto_c] = '╗'; L.append(r)

r = empty_row(); r[0] = '║'; r[W-1] = '║'
r[esp_c] = '▼'; r[cto_c] = '▼'; L.append(r)

# Especialista + CTO
esp_box = make_box([
    'Especialista Automotivo', '[general]', '● paused',
    'Domínio automotivo.', 'Valida diagnósticos,',
    'manuais e procedimentos.', 'Model: nemotron-3-super'
], esp_w)

cto_box = make_box([
    'CTO', '[cto]', '● paused',
    'Arquitetura, infra e', 'execução técnica do',
    'Auto Vision Agent.', 'Model: mimo-v2.5-free'
], cto_w)

# CTO bottom: add ╧ junction at cto_c
cto_box[-1][cto_c - cto_s] = '╧'

for i in range(max(len(esp_box), len(cto_box))):
    r = empty_row(); r[0] = '║'; r[W-1] = '║'
    if i < len(esp_box): insert_str(r, esp_s, ''.join(esp_box[i]))
    if i < len(cto_box): insert_str(r, cto_s, ''.join(cto_box[i]))
    L.append(r)

# Connector to engineers
r = empty_row(); r[0] = '║'; r[W-1] = '║'; r[cto_c] = '│'
L.append(r)

# Engineer branch
eng_w = 17; gap = 3
eng_s = [2 + i * (eng_w + gap) for i in range(4)]
eng_c = [s + eng_w // 2 for s in eng_s]

# ╔═══╤═══╤═══╧═══╤═══╗
r = empty_row(); r[0] = '║'; r[W-1] = '║'
r[eng_c[0]] = '╔'
r[eng_c[1]] = '╤'
r[eng_c[2]] = '╤'
r[cto_c] = '╧'
r[eng_c[3]] = '╤'
for c in range(eng_c[0]+1, eng_c[1]): r[c] = '═'
for c in range(eng_c[1]+1, eng_c[2]): r[c] = '═'
for c in range(eng_c[2]+1, cto_c): r[c] = '═'
for c in range(cto_c+1, eng_c[3]): r[c] = '═'
for c in range(eng_c[3]+1, eng_c[-1]): r[c] = '═'
r[eng_c[-1]] = '╗'; L.append(r)

r = empty_row(); r[0] = '║'; r[W-1] = '║'
for center in eng_c: r[center] = '▼'
L.append(r)

# Engineer boxes
eng_data = [
    ['Eng. Infra', '[devops]', '● paused', 'Gateway, GPU,', 'Docker, CI/CD', 'Model: laguna-m'],
    ['Eng. Dados', '[engineer]', '● paused', 'Dados automov.', 'fotos, manuais', 'TSBs, torque.', 'Model: mimo-v2.5'],
    ['Eng. Percepção', '[researcher]', '● error', 'Visão comput.', 'modelos multim.', 'Model: nemotron-'],
    ['Eng. Skills', '[engineer]', '● paused', 'Skills OpenClaw', 'auto-vision,', 'diagnóstico,RAG', 'Model: mimo-v2.5'],
]

eng_boxes = [make_box(d, eng_w) for d in eng_data]
max_lines = max(len(b) for b in eng_boxes)

for i in range(max_lines):
    r = empty_row(); r[0] = '║'; r[W-1] = '║'
    for bi, box in enumerate(eng_boxes):
        if i < len(box): insert_str(r, eng_s[bi], ''.join(box[i]))
    L.append(r)

L.append(make_content())
L.append(make_bottom())

for l in L:
    print(''.join(l))
