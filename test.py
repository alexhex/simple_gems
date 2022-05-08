# -*-coding:utf-8-*-

# Alexhex 05-03-2022

levels = '1223323423233'
letters = 'abcdefghijklm'

# keys = ('Name', 'Level')
ebom = []

# ebom = [row for row in ]
for (name, level) in zip(letters, levels):

    ebom.append(dict(Name=name, Level=int(level)))

# print(ebom)

row_num = -1
children = [set() for _ in levels]
# children[0].add('shit')
# print(children)
pos_group = [0] * 4
# pos_group[0].append(1)
# print(pos_group)

for row in ebom:
    row_num += 1
    pos_group[row['Level']-1] = row_num

    if row['Level'] >= 2:
        children[pos_group[row['Level']-2]].add(row['Name'])

print(children)
