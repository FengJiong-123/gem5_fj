import os
import sys
import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

#import assert

gem5_root = '/hpc2hdd/home/jfeng293/gem5_dir_fass/'
#job_file = 'bw_mem_submit_11_7'
#job_file = 'Multithread_all_11_16'
job_file = 'PlotTest'

#job_list = ['cachebw', 'bfs','kmeans','lud','nw']
job_list = ['bfs', 'hotspot3D', 'hotspot', 'pathfinder', 'srad', 'kmeans', 'lud']

Contiguous = [[] for i in range(len(job_list))]
Random     = [[] for i in range(len(job_list))]
Standrad   = [[] for i in range(len(job_list))]

#mkdir
if not os.path.exists(job_file):
    print("no such file", job_file)
    assert(0)

os.chdir(gem5_root+job_file)

for file in os.listdir(gem5_root+job_file):

    if '.sh' in file or '.err' in file or '.out' in file:
        continue

    file_words = file.split('_')
    Bench = file_words[0]
    Type  = file_words[1]

    if Type == '400' and not os.path.exists(gem5_root+job_file+'/'+Bench+'_401'):
        os.system('cp -r '+ gem5_root+job_file+'/'+file + ' ' + gem5_root+job_file+'/'+Bench+'_401' )


    if Type == '16120' and not os.path.exists(gem5_root+job_file+'/'+Bench+'_16121'):
        os.system('cp -r '+ gem5_root+job_file+'/'+file + ' ' + gem5_root+job_file+'/'+Bench+'_16121' )

    if Type == '100':
        if not os.path.exists(gem5_root+job_file+'/'+Bench+'_4121'):
            os.system('cp -r '+ gem5_root+job_file+'/'+file + ' ' + gem5_root+job_file+'/'+Bench+'_4121')
        if not os.path.exists(gem5_root+job_file+'/'+Bench+'_16601'):
            os.system('cp -r '+ gem5_root+job_file+'/'+file + ' ' + gem5_root+job_file+'/'+Bench+'_16601')

for file in os.listdir(gem5_root+job_file):

    if '.sh' in file or '.err' in file or '.out' in file:
        continue

    state_file = gem5_root+job_file+'/'+file + '/stats.txt'
    stats = open(state_file, 'r')

    ColPer= False
    Hit   = 0
    Miss  = 0
    Access= 0
    Evict = 0
    SnpClean = 0
    SnpCleanE= 0
    SnpFwd   = 0
    file_words = file.split('_')
    Bench = file_words[0]
    Type  = file_words[1]

    result = []
    result.append(file_words[0])
    result.append(file_words[1])

    lines = stats.readlines()
    if len(lines) < 3:
        print('No stats file')
        continue

    for line in lines:

        words = line.split()
        if len(words) < 1:
            continue
        if words[0] == 'finalTick':
            #print("   ",file)
            #print('Performance: ', words[1])
            if not ColPer:
                ColPer = True
            else:
                result.append(int(words[1]))
        
        if 'ruby' in words[0]:

            if 'm_dir_hits' in words[0]:
                #print('Hit: ', words[1])
                Hit += int(words[1])
                
            if 'm_dir_misses' in words[0]:
                #print('Miss: ', words[1])
                Miss += int(words[1])
                
            if 'm_dir_accesses' in words[0]:
                #print('Access: ', words[1])
                Access += int(words[1])
                
            if 'm_dir_evict' in words[0]:
                #print('Evict: ', words[1])
                Evict += int(words[1])
                
            if 'm_snp_clean' in words[0]:
                #print('SnpClean: ', words[1])
                SnpClean += int(words[1])
                
            if 'm_snp_evict_clean' in words[0]:
                #print('SnpClean: ', words[1])
                SnpCleanE += int(words[1])
                
            if 'm_snp_fwd' in words[0]:
                #print('SnpFwd: ', words[1])
                SnpFwd += int(words[1])

    #print("Hit: ", Hit,"  Miss: ",  Miss,"  Access: ",  Access,"  Evict: ",  Evict,"  SnpClean: ",  SnpClean,"  SnpCleanE: ",  SnpCleanE,"  SnpFwd: ",  SnpFwd)
    result.append(Access)
    result.append(Evict)
    result.append(SnpClean)
    result.append(SnpCleanE)
    result.append(SnpFwd)
    #print(result)
    if result[1] == '100' or result[1] == '10016':
        Contiguous[job_list.index(file_words[0])].append(result)
        Random[job_list.index(file_words[0])].append(result)
        Standrad[job_list.index(file_words[0])].append(result)
    elif result[1] == '400' or result[1] == '16120' or result[1] == '401' or result[1] == '161214' or result[1] == '40016' or result[1] == '40116':
        Contiguous[job_list.index(file_words[0])].append(result)
    elif result[1] == '440' or result[1] == '441' or result[1] == '16280' or result[1] == '16281' or result[1] == '416016' or result[1] == '416116':
        Random[job_list.index(file_words[0])].append(result)
    elif result[1] == '4120' or result[1] == '16600' or result[1] == '4121' or result[1] == '16601' or result[1] == '448016' or result[1] == '448116':
        Standrad[job_list.index(file_words[0])].append(result)
    else:
        assert(result[1] == '16121')
    stats.close()

assert(len(Contiguous) == len(Random) and len(Contiguous) == len(Standrad))

Contiguous_order = [['100', '400', '401', '16120', '161214'], ['10016', '40016', '40116']]
Random_order     = [['100', '440', '441', '16280', '16281'], ['10016', '416016', '416116']]
Standrad_order   = [['100', '4120','4121','16600', '16601'], ['10016', '448016', '448116']]

label = [['Full Bit', 'Cluster4', 'Cluster4_PST', 'Cluster16', 'Cluster16_PST'],
         ['Full Bit Thread16', 'Cluster4 Thread16', 'Cluster4_PST Thread16']]

assert(len(label) == len(Contiguous_order))

# make swap
for i in range(len(Contiguous)):
    for j in range(len(Contiguous[i])):
        for k in range(j, len(Contiguous[i])):
            if Contiguous[i][k][1] == Contiguous_order[int(j / len(Contiguous_order[0]))][int(j % len(Contiguous_order[0]))]:
                Contiguous[i][j], Contiguous[i][k] =  Contiguous[i][k], Contiguous[i][j]
                break
for i in range(len(Random)):
    for j in range(len(Random[i])):
        for k in range(j, len(Random[i])):
            if Random[i][k][1] == Random_order[int(j / len(Random_order[0]))][int(j % len(Random_order[0]))]:
                Random[i][j], Random[i][k] =  Random[i][k], Random[i][j]
                break
for i in range(len(Standrad)):
    for j in range(len(Standrad[i])):
        for k in range(j, len(Standrad[i])):
            if Standrad[i][k][1] == Standrad_order[int(j / len(Random_order[0]))][int(j % len(Random_order[0]))]:
                Standrad[i][j], Standrad[i][k] =  Standrad[i][k], Standrad[i][j]
                break

#print("\nAfter swap\n")
#print("Contiguous: ",Contiguous)
#print("Random:     ",Random)
#print("Standrad:   ",Standrad)

#start the plot
#print(Contiguous_Perf)
#color_list = ['red','orangered','salmon','coral','mistyrose','gold','darkorange','bisque']
color_list = ['royalblue','mediumslateblue','lightsteelblue','plum','mediumorchid','deeppink','violet','pink']

if not os.path.exists(gem5_root+'picture'):
    os.system('mkdir '+gem5_root+'picture')

fig = plt.figure(figsize=(18,9))
Contiguous_Perf = []
for i in range(len(Contiguous_order[0]) + len(Contiguous_order[1])):
    temp = []
    for j in range(len(Contiguous)):
        for k in range(len(Contiguous[j])):
            if Contiguous[j][k][1] == Contiguous_order[int(i / len(Contiguous_order[0]))][int(i % len(Contiguous_order[0]))]:
                if Contiguous[j][k][2] == 9333752530000:
                    print(Contiguous[j][k])
                if k < 5:
                    value = format(float(Contiguous[j][0][2])/float(Contiguous[j][k][2]), '.3f')
                    #temp.append(Contiguous[j][k][2])
                    if float(value) < 1.0:
                        temp.append(float(value))
                    else:
                        temp.append(1.0)
                else:
                    value = format(float(Contiguous[j][5][2])/float(Contiguous[j][k][2]), '.3f')
                    #temp.append(Contiguous[j][k][2])
                    if float(value) < 1.0:
                        temp.append(float(value))
                    else:
                        temp.append(1.0)

    Contiguous_Perf.append(temp)

x = np.arange(len(job_list))
total_width, n = 0.8, len(Contiguous_order[0])
width = total_width / n
x = x - (total_width - width) / 2
start = x[0]

ax1 = fig.add_subplot(311)
plt.ylim((0.55, 1.2))
plt.title('Contiguous', fontsize=16, fontweight='bold')
for i in range(len(Contiguous_order[0])):
    plt.bar(x+i*width, Contiguous_Perf[i], width = width*7/8, label = label[0][i], fc=color_list[i])

x = np.arange(len(job_list)+1, 2*len(job_list)+1, 1)
x = x - (total_width - width) / 2
'''
for i in range(len(Contiguous_order[1])):
    if not i == 0:
        plt.bar(x+i*width, Contiguous_Perf[i+len(Contiguous_order[0])], width = width, label = label[1][i], fc=color_list[i])
    else:
        plt.bar(x+i*width, Contiguous_Perf[i+len(Contiguous_order[0])], width = width, label = label[1][i], fc=color_list[i])
        '''
plt.legend(ncol = 5, loc='upper right')
plt.ylabel('Speed up over Full bit')

my_xlabel = []
my_xAxis = []
#for j in range(len(Contiguous_order)):
for i in range(len(job_list)):
    my_xlabel.append(job_list[i])

for i in range(len(my_xlabel)):
    my_xAxis.append(start + i*len(Contiguous_order[0])*width*1.25 + int(i / len(job_list)))

plt.xticks(my_xAxis, my_xlabel,rotation=0, ha='right', fontsize=10)

plt.savefig(gem5_root+'picture/Contiguous.pdf', bbox_inches='tight')


Random_Perf = []
for i in range(len(Random_order[0]) + len(Random_order[1])):
    temp = []
    for j in range(len(Random)):
        for k in range(len(Random[j])):
            if Random[j][k][1] == Random_order[int(i / len(Random_order[0]))][int(i % len(Random_order[0]))]:
                if Random[j][k][2] == 9333752530000:
                    print(Random[j][k])
                if k < 5:
                    value = format(float(Random[j][0][2])/float(Random[j][k][2]), '.3f')
                    #temp.append(Random[j][k][2])
                    if float(value) < 1.0:
                        temp.append(float(value))
                    else:
                        temp.append(1.0)
                else:
                    value = format(float(Random[j][5][2])/float(Random[j][k][2]), '.3f')
                    #temp.append(Random[j][k][2])
                    if float(value) < 1.0:
                        temp.append(float(value))
                    else:
                        temp.append(1.0)

    Random_Perf.append(temp)

x = np.arange(len(job_list))
total_width, n = 0.8, len(Random_order[0])
width = total_width / n
x = x - (total_width - width) / 2
start = x[0]

ax1 = fig.add_subplot(312)
plt.ylim((0.55, 1.2))
plt.title('Random', fontsize=16, fontweight='bold')
for i in range(len(Random_order[0])):
    plt.bar(x+i*width, Random_Perf[i], width = width*7/8, label = label[0][i], fc=color_list[i])

x = np.arange(len(job_list)+1, 2*len(job_list)+1, 1)
x = x - (total_width - width) / 2
'''
for i in range(len(Random_order[1])):
    if not i == 0:
        plt.bar(x+i*width, Random_Perf[i+len(Random_order[0])], width = width, label = label[1][i], fc=color_list[i])
    else:
        plt.bar(x+i*width, Random_Perf[i+len(Random_order[0])], width = width, label = label[1][i], fc=color_list[i])
        '''
plt.legend(ncol = 5, loc='upper right')
plt.ylabel('Speed up over Full bit')

my_xlabel = []
my_xAxis = []
#for j in range(len(Random_order)):
for i in range(len(job_list)):
    my_xlabel.append(job_list[i])

for i in range(len(my_xlabel)):
    my_xAxis.append(start + i*len(Random_order[0])*width*1.25 + int(i / len(job_list)))

plt.xticks(my_xAxis, my_xlabel,rotation=0, ha='right', fontsize=10)


Standrad_Perf = []
for i in range(len(Standrad_order[0]) + len(Standrad_order[1])):
    temp = []
    for j in range(len(Standrad)):
        for k in range(len(Standrad[j])):
            if Standrad[j][k][1] == Standrad_order[int(i / len(Standrad_order[0]))][int(i % len(Standrad_order[0]))]:
                if Standrad[j][k][2] == 9333752530000:
                    print(Standrad[j][k])
                if k < 5:
                    value = format(float(Standrad[j][0][2])/float(Standrad[j][k][2]), '.3f')
                    #temp.append(Standrad[j][k][2])
                    if float(value) < 1.0:
                        temp.append(float(value))
                    else:
                        temp.append(1.0)
                else:
                    value = format(float(Standrad[j][5][2])/float(Standrad[j][k][2]), '.3f')
                    #temp.append(Standrad[j][k][2])
                    if float(value) < 1.0:
                        temp.append(float(value))
                    else:
                        temp.append(1.0)

    Standrad_Perf.append(temp)

x = np.arange(len(job_list))
total_width, n = 0.8, len(Standrad_order[0])
width = total_width / n
x = x - (total_width - width) / 2
start = x[0]

ax1 = fig.add_subplot(313)
plt.ylim((0.55, 1.2))
plt.title('Standrad', fontsize=16, fontweight='bold')
for i in range(len(Standrad_order[0])):
    plt.bar(x+i*width, Standrad_Perf[i], width = width*7/8, label = label[0][i], fc=color_list[i])

x = np.arange(len(job_list)+1, 2*len(job_list)+1, 1)
x = x - (total_width - width) / 2
'''
for i in range(len(Standrad_order[1])):
    if not i == 0:
        plt.bar(x+i*width, Standrad_Perf[i+len(Standrad_order[0])], width = width, label = label[1][i], fc=color_list[i])
    else:
        plt.bar(x+i*width, Standrad_Perf[i+len(Standrad_order[0])], width = width, label = label[1][i], fc=color_list[i])
        '''
plt.legend(ncol = 5, loc='upper right')
plt.ylabel('Speed up over Full bit')

my_xlabel = []
my_xAxis = []
#for j in range(len(Standrad_order)):
for i in range(len(job_list)):
    my_xlabel.append(job_list[i])

for i in range(len(my_xlabel)):
    my_xAxis.append(start + i*len(Standrad_order[0])*width*1.25 + int(i / len(job_list)))

plt.xticks(my_xAxis, my_xlabel,rotation=0, ha='right', fontsize=10)
plt.savefig(gem5_root+'picture/Standard.pdf', bbox_inches='tight')







# collect the snoop number
fig1 = plt.figure(figsize=(18,10.5))
SnoopType = ['SnpClean', 'SnpCleanEvict', 'SnpShared']
OrderSnoopType = []
for i in range(len(Contiguous_order[0])):
    for j in range(len(SnoopType)):
        OrderSnoopType.append(Contiguous_order[0][i]+'_'+SnoopType[j])
#print(OrderSnoopType)

Contiguous_snoop = [[] for i in range(len(OrderSnoopType))]
total_snoop_cnt = []
access_cnt = []
for i in range(len(Contiguous)):
    for j in range(0, len(Contiguous[i]) - len(Contiguous_order[1])):
        if len(Contiguous[i][j]) > 7:
            assert(len(Contiguous[i][j]) == 8)
            total_snoop = Contiguous[i][0][5] + Contiguous[i][0][6]+ Contiguous[i][0][7]
            #total_snoop = Contiguous[i][j][5] + Contiguous[i][j][6]+ Contiguous[i][j][7]
            #ratio = 
            if j == 0:
                total_snoop_cnt.append(str(total_snoop))
                access_cnt.append(str(Contiguous[i][0][3]))
            for k in range(5, len(Contiguous[i][j])):
                value = format(float(Contiguous[i][j][k])/float(total_snoop), '.4f')
                #assert(float(value) < 1.0)
                Contiguous_snoop[k+j*len(SnoopType)-5].append(float(value))
        else:
            assert(len(Contiguous[i][j]) == 7)
            total_snoop = Contiguous[i][0][4] + Contiguous[i][0][5]+ Contiguous[i][0][6]
            #total_snoop = Contiguous[i][j][4] + Contiguous[i][j][5]+ Contiguous[i][j][6]
            if j == 0:
                total_snoop_cnt.append(str(total_snoop))
                access_cnt.append(str(Contiguous[i][0][2]))
            for k in range(4, len(Contiguous[i][j])):
                value = format(float(Contiguous[i][j][k])/float(total_snoop), '.4f')
                #assert(float(value) < 1.0)
                Contiguous_snoop[k+j*len(SnoopType)-4].append(float(value))

color_list_cnt = ['darkolivegreen','limegreen','khaki']
x = np.arange(len(job_list))
total_width, n = 0.8, len(OrderSnoopType)
width = total_width / n
x = x - (total_width - width) / 2

ax4 = fig1.add_subplot(311)
#plt.yscale('log', base=4)
plt.ylim((0, 17))
plt.title('Snoop of Contiguous', fontsize=16, fontweight='bold')
my_xlabel = []
my_xAxis = []
for i in range(len(OrderSnoopType)):
    if i > 2:
        if i % len(SnoopType) == 0:
            plt.bar(x+int(i/len(SnoopType))*len(SnoopType) *width, Contiguous_snoop[i], width = len(SnoopType) * width*7/8, fc=color_list_cnt[int(i%len(SnoopType))])
        elif i % len(SnoopType) == 1:
            plt.bar(x+int(i/len(SnoopType))*len(SnoopType)*width, Contiguous_snoop[i], width = len(SnoopType) *width*7/8, bottom=Contiguous_snoop[i-1], fc=color_list_cnt[int(i%len(SnoopType))])
        elif i % len(SnoopType) == 2:
            Bottom = np.add(Contiguous_snoop[i-1], Contiguous_snoop[i-2])
            plt.bar(x+int(i/len(SnoopType))*len(SnoopType)*width, Contiguous_snoop[i], width = len(SnoopType) *width*7/8, bottom=Bottom, fc=color_list_cnt[int(i%len(SnoopType))])

    else:
        if i % len(SnoopType) == 0:
            plt.bar(x+int(i/len(SnoopType))*len(SnoopType)*width, Contiguous_snoop[i], width = len(SnoopType) *width*7/8, label = SnoopType[i], fc=color_list_cnt[int(i%len(SnoopType))])
        elif i % len(SnoopType) == 1:
            plt.bar(x+int(i/len(SnoopType))*len(SnoopType)*width, Contiguous_snoop[i], width = len(SnoopType) *width*7/8, bottom=Contiguous_snoop[i-1], label = SnoopType[i], fc=color_list_cnt[int(i%len(SnoopType))])
        elif i % len(SnoopType) == 2:
            Bottom = np.add(Contiguous_snoop[i-1], Contiguous_snoop[i-2])
            plt.bar(x+int(i/len(SnoopType))*len(SnoopType)*width, Contiguous_snoop[i], width = len(SnoopType) *width*7/8, bottom=Bottom,label = SnoopType[i], fc=color_list_cnt[int(i%len(SnoopType))])


for i in range(len(job_list)):
    for j in range(len(Contiguous_order[0])):
        my_xlabel.append(label[0][j])

for i in range(len(my_xlabel)):
    my_xAxis.append(x[0] + i*len(SnoopType)*width + float(int(i / len(Contiguous_order[0]))) * 0.2)

for i in range(len(job_list)):
    plt.text(x[0] + 0.2 +i, -5, job_list[i], fontsize=14, color='black')
    plt.text(x[0] +i, 13, 'Full bit:', fontsize=10, color='black')
    plt.text(x[0] +i, 11, 'Access: '+access_cnt[i], fontsize=10, color='black')
    plt.text(x[0] +i, 9, 'Total Snp: '+total_snoop_cnt[i], fontsize=10, color='black')

plt.xticks(my_xAxis, my_xlabel,rotation=20, ha='right', fontsize=10) 
plt.legend(ncol = 5)
plt.ylabel('Normalize break-down to full bit')

plt.savefig(gem5_root+'picture/ContiguousSnoop.pdf', bbox_inches='tight')



Random_snoop = [[] for i in range(len(OrderSnoopType))]
total_snoop_cnt = []
access_cnt = []
for i in range(len(Random)):
    for j in range(0, len(Random[i]) - len(Random_order[1])):
        if len(Random[i][j]) > 7:
            assert(len(Random[i][j]) == 8)
            total_snoop = Random[i][0][5] + Random[i][0][6]+ Random[i][0][7]
            #ratio = 
            if j == 0:
                total_snoop_cnt.append(str(total_snoop))
                access_cnt.append(str(Random[i][0][3]))
            for k in range(5, len(Random[i][j])):
                value = format(float(Random[i][j][k])/float(total_snoop), '.4f')
                #assert(float(value) < 1.0)
                Random_snoop[k+j*len(SnoopType)-5].append(float(value))
        else:
            assert(len(Random[i][j]) == 7)
            total_snoop = Random[i][0][4] + Random[i][0][5]+ Random[i][0][6]

            if j == 0:
                total_snoop_cnt.append(str(total_snoop))
                access_cnt.append(str(Random[i][0][2]))
            for k in range(4, len(Random[i][j])):
                value = format(float(Random[i][j][k])/float(total_snoop), '.4f')
                #assert(float(value) < 1.0)
                CRandom_snoop[k+j*len(SnoopType)-4].append(float(value))

color_list_cnt = ['darkolivegreen','limegreen','khaki']
x = np.arange(len(job_list))
total_width, n = 0.8, len(OrderSnoopType)
width = total_width / n
x = x - (total_width - width) / 2

ax4 = fig1.add_subplot(312)
#plt.yscale('log', base=4)
plt.ylim((0, 17))
plt.title('Snoop of Random', fontsize=16, fontweight='bold')
my_xlabel = []
my_xAxis = []
for i in range(len(OrderSnoopType)):
    if i > 2:
        if i % len(SnoopType) == 0:
            plt.bar(x+int(i/len(SnoopType))*len(SnoopType) *width, Random_snoop[i], width = len(SnoopType) * width*7/8, fc=color_list_cnt[int(i%len(SnoopType))])
        elif i % len(SnoopType) == 1:
            plt.bar(x+int(i/len(SnoopType))*len(SnoopType)*width, Random_snoop[i], width = len(SnoopType) *width*7/8, bottom=Random_snoop[i-1], fc=color_list_cnt[int(i%len(SnoopType))])
        elif i % len(SnoopType) == 2:
            Bottom = np.add(Random_snoop[i-1], Random_snoop[i-2])
            plt.bar(x+int(i/len(SnoopType))*len(SnoopType)*width, Random_snoop[i], width = len(SnoopType) *width*7/8, bottom=Bottom, fc=color_list_cnt[int(i%len(SnoopType))])

    else:
        if i % len(SnoopType) == 0:
            plt.bar(x+int(i/len(SnoopType))*len(SnoopType)*width, Random_snoop[i], width = len(SnoopType) *width*7/8, label = SnoopType[i], fc=color_list_cnt[int(i%len(SnoopType))])
        elif i % len(SnoopType) == 1:
            plt.bar(x+int(i/len(SnoopType))*len(SnoopType)*width, Random_snoop[i], width = len(SnoopType) *width*7/8, bottom=Random_snoop[i-1], label = SnoopType[i], fc=color_list_cnt[int(i%len(SnoopType))])
        elif i % len(SnoopType) == 2:
            Bottom = np.add(Random_snoop[i-1], Random_snoop[i-2])
            plt.bar(x+int(i/len(SnoopType))*len(SnoopType)*width, Random_snoop[i], width = len(SnoopType) *width*7/8, bottom=Bottom,label = SnoopType[i], fc=color_list_cnt[int(i%len(SnoopType))])


for i in range(len(job_list)):
    for j in range(len(Random_order[0])):
        my_xlabel.append(label[0][j])

for i in range(len(my_xlabel)):
    my_xAxis.append(x[0] + i*len(SnoopType)*width + float(int(i / len(Random_order[0]))) * 0.2)

for i in range(len(job_list)):
    plt.text(x[0] + 0.2 +i, -5, job_list[i], fontsize=14, color='black')
    plt.text(x[0] +i, 13, 'Full bit:', fontsize=10, color='black')
    plt.text(x[0] +i, 11, 'Access: '+access_cnt[i], fontsize=10, color='black')
    plt.text(x[0] +i, 9, 'Total Snp: '+total_snoop_cnt[i], fontsize=10, color='black')

plt.xticks(my_xAxis, my_xlabel,rotation=20, ha='right', fontsize=10) 
plt.legend(ncol = 5)
plt.ylabel('Normalize break-down to full bit')
#plt.savefig(gem5_root+'picture/RandomSnoop.pdf', bbox_inches='tight')


Standrad_snoop = [[] for i in range(len(OrderSnoopType))]
total_snoop_cnt = []
access_cnt = []
for i in range(len(Standrad)):
    for j in range(0, len(Standrad[i]) - len(Standrad_order[1])):
        if len(Standrad[i][j]) > 7:
            assert(len(Standrad[i][j]) == 8)
            total_snoop = Standrad[i][0][5] + Standrad[i][0][6]+ Standrad[i][0][7]
            
            if j == 0:
                total_snoop_cnt.append(str(total_snoop))
                access_cnt.append(str(Standrad[i][0][3]))
            for k in range(5, len(Standrad[i][j])):
                value = format(float(Standrad[i][j][k])/float(total_snoop), '.4f')
                #assert(float(value) < 1.0)
                Standrad_snoop[k+j*len(SnoopType)-5].append(float(value))
        else:
            assert(len(Standrad[i][j]) == 7)
            total_snoop = Standrad[i][0][4] + Standrad[i][0][5]+ Standrad[i][0][6]
        
            if j == 0:
                total_snoop_cnt.append(str(total_snoop))
                access_cnt.append(str(Standrad[i][0][2]))
            for k in range(4, len(Standrad[i][j])):
                value = format(float(Standrad[i][j][k])/float(total_snoop), '.4f')
                #assert(float(value) < 1.0)
                Standrad_snoop[k+j*len(SnoopType)-4].append(float(value))

color_list_cnt = ['darkolivegreen','limegreen','khaki']
x = np.arange(len(job_list))
total_width, n = 0.8, len(OrderSnoopType)
width = total_width / n
x = x - (total_width - width) / 2

ax4 = fig1.add_subplot(313)
#plt.yscale('log', base=4)
plt.ylim((0, 17))
plt.title('Snoop of Standrad', fontsize=16, fontweight='bold')
my_xlabel = []
my_xAxis = []
for i in range(len(OrderSnoopType)):
    if i > 2:
        if i % len(SnoopType) == 0:
            plt.bar(x+int(i/len(SnoopType))*len(SnoopType) *width, Standrad_snoop[i], width = len(SnoopType) * width*7/8, fc=color_list_cnt[int(i%len(SnoopType))])
        elif i % len(SnoopType) == 1:
            plt.bar(x+int(i/len(SnoopType))*len(SnoopType)*width, Standrad_snoop[i], width = len(SnoopType) *width*7/8, bottom=Standrad_snoop[i-1], fc=color_list_cnt[int(i%len(SnoopType))])
        elif i % len(SnoopType) == 2:
            Bottom = np.add(Standrad_snoop[i-1], Standrad_snoop[i-2])
            plt.bar(x+int(i/len(SnoopType))*len(SnoopType)*width, Standrad_snoop[i], width = len(SnoopType) *width*7/8, bottom=Bottom, fc=color_list_cnt[int(i%len(SnoopType))])

    else:
        if i % len(SnoopType) == 0:
            plt.bar(x+int(i/len(SnoopType))*len(SnoopType)*width, Standrad_snoop[i], width = len(SnoopType) *width*7/8, label = SnoopType[i], fc=color_list_cnt[int(i%len(SnoopType))])
        elif i % len(SnoopType) == 1:
            plt.bar(x+int(i/len(SnoopType))*len(SnoopType)*width, Standrad_snoop[i], width = len(SnoopType) *width*7/8, bottom=Standrad_snoop[i-1], label = SnoopType[i], fc=color_list_cnt[int(i%len(SnoopType))])
        elif i % len(SnoopType) == 2:
            Bottom = np.add(Standrad_snoop[i-1], Standrad_snoop[i-2])
            plt.bar(x+int(i/len(SnoopType))*len(SnoopType)*width, Standrad_snoop[i], width = len(SnoopType) *width*7/8, bottom=Bottom,label = SnoopType[i], fc=color_list_cnt[int(i%len(SnoopType))])


for i in range(len(job_list)):
    for j in range(len(Standrad_order[0])):
        my_xlabel.append(label[0][j])

for i in range(len(my_xlabel)):
    my_xAxis.append(x[0] + i*len(SnoopType)*width + float(int(i / len(Standrad_order[0]))) * 0.2)

for i in range(len(job_list)):
    plt.text(x[0] + 0.2 +i, -5, job_list[i], fontsize=14, color='black')
    plt.text(x[0] +i, 13, 'Full bit:', fontsize=10, color='black')
    plt.text(x[0] +i, 11, 'Access: '+access_cnt[i], fontsize=10, color='black')
    plt.text(x[0] +i, 9, 'Total Snp: '+total_snoop_cnt[i], fontsize=10, color='black')

plt.xticks(my_xAxis, my_xlabel,rotation=20, ha='right', fontsize=10) 
plt.legend(ncol = 5)
plt.ylabel('Normalize break-down to full bit')

plt.tight_layout()
plt.savefig(gem5_root+'picture/StandardSnoop.pdf', bbox_inches='tight')