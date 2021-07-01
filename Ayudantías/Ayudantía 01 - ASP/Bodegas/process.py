import sys

lines = sys.stdin.readlines()

init = len(lines) - 1
while "on(" not in lines[init]:
    init -= 1

atoms = lines[init].split(" ")

obstacles = []

rangoX = []
rangoY = []


for line in atoms:
    if line[0:6] != "rangeX":
        continue
    line = line.replace("rangeX", "")
    line = line.replace("(", "")
    line = line.replace(")", "")
    rangoX.append(int(line))

for line in atoms:
    if line[0:6] != "rangeY":
        continue
    line = line.replace("rangeY", "")
    line = line.replace("(", "")
    line = line.replace(")", "")
    rangoY.append(int(line))


for line in atoms:
    if line[0:3] != "obs":
        continue
    line = line.replace("obstacle", "")
    line = line.replace("(", "")
    line = line.replace(")", "")
    tup = line.split(",")
    obstacles.append([int(tup[0]), int(tup[1])])

en = []
for line in atoms:
    if line[0:3] != "on(":
        continue
    line = line.replace("on(", "")
    line = line.replace(")", "")
    tup = line.split(",")
    en.append([int(tup[0])-1, int(tup[1]), int(tup[2]), int(tup[3])])

objectives = []
for line in atoms:
    if line[0:3] != "goa":
        continue
    line = line.replace("goal", "")
    line = line.replace("(", "")
    line = line.replace(")", "")
    tup = line.split(",")
    objectives.append([int(tup[0])-1, int(tup[1]), int(tup[2]), int(tup[3])])

robots = []
for t in en:
    if t[0] not in robots:
        robots.append(t[0])

times = []
for t in en:
    if t[3] not in times:
        times.append(t[3])
times.sort()

en.sort(key=lambda x: x[3])
en.sort(key=lambda x: x[0])

pos = {}

for r in robots:
    pos['rob_' + str(r)] = []

for t in en:
    pos['rob_' + str(t[0])].append([t[1], t[2]])


print('var xrange;')
print('var yrange;')
print('xrange=', max(rangoX), ';')
print('yrange=', max(rangoY), ';')

print('var objectives=[];')
for t in times:
    print('objectives[' + str(t) + ']=', [[r, x, y] for [r, x, y, time] in objectives if time == t])

print('var obstacles;')
print('obstacles=', obstacles)

print('var pos=[];')
i = 0
for r in robots:
    print('pos[' + str(i) + ']=', pos['rob_' + str(r)], ';')
    i += 1

print('var events=[]')
for t in times:
    print('events[' + str(t) + ']=', [[r, x, y] for [r, x, y, time] in en if time == t])
