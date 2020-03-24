import matplotlib.pyplot as plt

fig = plt.figure(figsize = (30, 6))
ax = fig.subplots(1, 3)

fp = open('./redis_set.txt', 'r')

no_y = []
no_x = []

rdb_y = []
rdb_x = []

aof_y = []
aof_x = []

cri = 0

while True:
    line = fp.readline()
    if not line : 
        break
    if line == "rdb_start\n" and cri == 0 :
        cri = 1
        continue
    elif line == "rdb_end\n" and cri == 1 : 
        cri = 0
        continue
    elif line == "aof_start\n" and cri == 0:
        cri = 2
        continue
    elif line == "aof_end\n" and cri == 2 :
        cri = 0
        continue
    
    if cri == 0:
        no_y.append(float(line))
    elif cri == 1:
        rdb_y.append(float(line))
    elif cri == 2:
        aof_y.append(float(line))

fp.close()

for i in range(0, len(rdb_y)):
    rdb_x.append(i)

for i in range(0, len(aof_y)):
    aof_x.append(i)

for i in range(0, len(no_y)):
    no_x.append(i)

ax[0].set_ylabel('NO-RDB-AOF-LATENCHY')
ax[0].set_xlabel('SET-COMMAND-COUNT')

ax[1].set_ylabel('RDB-LATENCHY')
ax[1].set_xlabel('SET-COMMAND-COUNT')

ax[2].set_ylabel('AOF-LATENCHY')
ax[2].set_xlabel('SET-COMMAND-COUNT')

ax[0].plot(no_x, no_y)
ax[1].plot(rdb_x, rdb_y)
ax[2].plot(aof_x, aof_y)

plt.show()
