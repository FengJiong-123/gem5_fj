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
job_list = ['bfs', 'hotspot3D', 'hotspot', 'pathfinder', 'srad', 'kmeans']

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

Contiguous_order = ['100', '400', '401', '16120', '161214', '10016', '40016', '40116']
Random_order     = ['100', '440', '441', '16280', '16281', '10016', '416016', '416116']
Standrad_order   = ['100', '4120','4121','16600', '16601', '10016', '448016', '448116']

label = ['Full Bit Thread4', 'Cluster4 Thread4', 'Cluster4_PST Thread4', 'Cluster16 Thread4', 'Cluster16_PST Thread4',
         'Full Bit Thread16', 'Cluster4 Thread16', 'Cluster4_PST Thread16']

assert(len(label) == len(Contiguous_order))

# make swap
for i in range(len(Contiguous)):
    for j in range(len(Contiguous[i])):
        for k in range(j, len(Contiguous[i])):
            if Contiguous[i][k][1] == Contiguous_order[j]:
                Contiguous[i][j], Contiguous[i][k] =  Contiguous[i][k], Contiguous[i][j]
                break
for i in range(len(Random)):
    for j in range(len(Random[i])):
        for k in range(j, len(Random[i])):
            if Random[i][k][1] == Random_order[j]:
                Random[i][j], Random[i][k] =  Random[i][k], Random[i][j]
                break
for i in range(len(Standrad)):
    for j in range(len(Standrad[i])):
        for k in range(j, len(Standrad[i])):
            if Standrad[i][k][1] == Standrad_order[j]:
                Standrad[i][j], Standrad[i][k] =  Standrad[i][k], Standrad[i][j]
                break

#print("\nAfter swap\n")
#print("Contiguous: ",Contiguous)
#print("Random:     ",Random)
#print("Standrad:   ",Standrad)

#start the plot
#print(Contiguous_Perf)
#color_list = ['red','orangered','salmon','coral','mistyrose','gold','darkorange','bisque']
color_list = ['royalblue','mediumslateblue','lightsteelblue','plum','mediumorchid','deeppink','coral','pink']

if not os.path.exists(gem5_root+'picture'):
    os.system('mkdir '+gem5_root+'picture')

Contiguous_Perf = []
for i in range(len(Contiguous_order)):
    temp = []
    for j in range(len(Contiguous)):
        for k in range(len(Contiguous[j])):
            if Contiguous[j][k][1] == Contiguous_order[i]:
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
total_width, n = 0.8, len(Contiguous_order)
width = total_width / n
x = x - (total_width - width) / 2

plt.figure(figsize=(18,3))
plt.ylim((0.55, 1.2))
plt.title('Contiguous', fontsize=16, fontweight='bold')
for i in range(len(Contiguous_order)):
    if not i == 0:
        plt.bar(x+i*width, Contiguous_Perf[i], width = width, label = label[i], fc=color_list[i])
    else:
        plt.bar(x+i*width, Contiguous_Perf[i], width = width, label = label[i], tick_label = job_list, fc=color_list[i])
plt.legend(ncol = 4)
plt.savefig(gem5_root+'picture/Contiguous.pdf', bbox_inches='tight')


Random_Perf = []
for i in range(len(Random_order)):
    temp = []
    for j in range(len(Random)):
        for k in range(len(Random[j])):
            if Random[j][k][1] == Random_order[i]:
                if Random[j][k][2] == 9333752530000:
                    print(Random[j][k])
                if k < 5:
                    value = format(float(Random[j][0][2])/float(Random[j][k][2]), '.3f')
                    #temp.append(Random[j][k][2])
                    #if k == 4 and Random[j][0][0] == 'hotspot':
                    #    print(value, Random[j][0][2], Random[j][k][2])
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
total_width, n = 0.8, len(Random_order)
width = total_width / n
x = x - (total_width - width) / 2

plt.figure(figsize=(18,3))
plt.ylim((0.55, 1.2))
plt.title('Random', fontsize=16, fontweight='bold')
for i in range(len(Random_order)):
    if not i == 0:
        plt.bar(x+i*width, Random_Perf[i], width = width, label = label[i], fc=color_list[i])
    else:
        plt.bar(x+i*width, Random_Perf[i], width = width, label = label[i], tick_label = job_list, fc=color_list[i])
plt.legend(ncol = 4)
plt.savefig(gem5_root+'picture/Random.pdf', bbox_inches='tight')


Standrad_Perf = []
for i in range(len(Standrad_order)):
    temp = []
    for j in range(len(Standrad)):
        for k in range(len(Standrad[j])):
            if Standrad[j][k][1] == Standrad_order[i]:
                if k < 5:
                    if Standrad[j][k][2] == 9333752530000:
                        print(Standrad[j][k])
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
total_width, n = 0.8, len(Standrad_order)
width = total_width / n
x = x - (total_width - width) / 2

plt.figure(figsize=(18,3))
plt.ylim((0.55, 1.2))
plt.title('Standard', fontsize=16, fontweight='bold')
for i in range(len(Standrad_order)):
    if not i == 0:
        plt.bar(x+i*width, Standrad_Perf[i], width = width, label = label[i], fc=color_list[i])
    else:
        plt.bar(x+i*width, Standrad_Perf[i], width = width, label = label[i], tick_label = job_list, fc=color_list[i])
plt.legend(ncol = 4)
plt.savefig(gem5_root+'picture/Standard.pdf', bbox_inches='tight')

# collect the snoop number
SnoopType = ['Access', 'Evict', 'SnpClean', 'SnpCleanEvict', 'SnpShared']
OrderSnoopType = []
for i in range(len(Contiguous_order)):
    for j in range(len(SnoopType)):
        OrderSnoopType.append(Contiguous_order[i]+'_'+SnoopType[j])
#print(OrderSnoopType)

Contiguous_snoop = [[] for i in range(len(OrderSnoopType))]
for i in range(len(Contiguous)):
    for j in range(len(Contiguous[i])):
        if len(Contiguous[i][j]) > 7:
            assert(len(Contiguous[i][j]) == 8)
            for k in range(3, len(Contiguous[i][j])):
                Contiguous_snoop[k+j*len(SnoopType)-3].append(Contiguous[i][j][k])
        else:
            assert(len(Contiguous[i][j]) == 7)
            for k in range(2, len(Contiguous[i][j])):
                Contiguous_snoop[k+j*len(SnoopType)-2].append(Contiguous[i][j][k])
##print(Contiguous_snoop)


color_list_cnt = ['darkolivegreen','green','limegreen','yellowgreen','khaki']
x = np.arange(len(job_list))
total_width, n = 0.8, len(OrderSnoopType)
width = total_width / n
x = x - (total_width - width) / 2
#print(x)
#print(width)

plt.figure(figsize=(18,3))
plt.yscale('log', base=4)
plt.ylim((4, 400000000))
plt.title('Snoop of Contiguous', fontsize=16, fontweight='bold')
my_xlabel = []
my_xAxis = []
for i in range(len(OrderSnoopType)):
    if i > 4:
        plt.bar(x+i*width, Contiguous_snoop[i], width = width, fc=color_list_cnt[int(i%len(SnoopType))])
    else:
        plt.bar(x+i*width, Contiguous_snoop[i], width = width, label = SnoopType[i], fc=color_list_cnt[int(i%len(SnoopType))])

for i in range(len(job_list)):
    for j in range(len(Contiguous_order)):
        my_xlabel.append(label[j])

for i in range(len(my_xlabel)):
    my_xAxis.append(x[0] + i*len(SnoopType)*width + float(int(i / len(Contiguous_order))) * 0.2)

for i in range(len(job_list)):
    plt.text(x[0] + 0.4 + i, 100000000, job_list[i], fontsize=14, color='black')
#my_xAxis = np.arange(0- (total_width - width) / 2,len(job_list)- (total_width - width) / 2, (1 / len(Contiguous_order)))
#print(my_xlabel)
#print(my_xAxis)
plt.xticks(my_xAxis, my_xlabel,rotation=20, ha='right') 
plt.legend(ncol = 5)
plt.savefig(gem5_root+'picture/ContiguousSnoop.pdf', bbox_inches='tight')



Random_snoop = [[] for i in range(len(OrderSnoopType))]
for i in range(len(Random)):
    for j in range(len(Random[i])):
        if len(Random[i][j]) > 7:
            assert(len(Random[i][j]) == 8)
            for k in range(3, len(Random[i][j])):
                Random_snoop[k+j*len(SnoopType)-3].append(Random[i][j][k])
        else:
            assert(len(Random[i][j]) == 7)
            for k in range(2, len(Random[i][j])):
                Random_snoop[k+j*len(SnoopType)-2].append(Random[i][j][k])

plt.figure(figsize=(18,3))
plt.yscale('log', base=4)
plt.ylim((4, 400000000))
plt.title('Snoop of Random', fontsize=16, fontweight='bold')
my_xlabel = []
my_xAxis = []
for i in range(len(OrderSnoopType)):
    if i > 4:
        plt.bar(x+i*width, Random_snoop[i], width = width, fc=color_list_cnt[int(i%len(SnoopType))])
    else:
        plt.bar(x+i*width, Random_snoop[i], width = width, label = SnoopType[i], fc=color_list_cnt[int(i%len(SnoopType))])

for i in range(len(job_list)):
    for j in range(len(Random_order)):
        my_xlabel.append(label[j])

for i in range(len(my_xlabel)):
    my_xAxis.append(x[0] + i*len(SnoopType)*width + float(int(i / len(Random_order))) * 0.2)

for i in range(len(job_list)):
    plt.text(x[0] + 0.4 + i, 100000000, job_list[i], fontsize=14, color='black')

#print(my_xlabel)
#print(my_xAxis)
plt.xticks(my_xAxis, my_xlabel,rotation=20, ha='right') 
plt.legend(ncol = 5)
plt.savefig(gem5_root+'picture/RandomSnoop.pdf', bbox_inches='tight')


Standrad_snoop = [[] for i in range(len(OrderSnoopType))]
for i in range(len(Standrad)):
    for j in range(len(Standrad[i])):
        if len(Standrad[i][j]) > 7:
            assert(len(Standrad[i][j]) == 8)
            for k in range(3, len(Standrad[i][j])):
                Standrad_snoop[k+j*len(SnoopType)-3].append(Standrad[i][j][k])
        else:
            assert(len(Standrad[i][j]) == 7)
            for k in range(2, len(Standrad[i][j])):
                Standrad_snoop[k+j*len(SnoopType)-2].append(Standrad[i][j][k])


plt.figure(figsize=(18,3))
plt.yscale('log', base=4)
plt.ylim((4, 400000000))
plt.title('Snoop of Standard', fontsize=16, fontweight='bold')
my_xlabel = []
my_xAxis = []
for i in range(len(OrderSnoopType)):
    if i > 4:
        plt.bar(x+i*width, Standrad_snoop[i], width = width, fc=color_list_cnt[int(i%len(SnoopType))])
    else:
        plt.bar(x+i*width, Standrad_snoop[i], width = width, label = SnoopType[i], fc=color_list_cnt[int(i%len(SnoopType))])

for i in range(len(job_list)):
    for j in range(len(Standrad_order)):
        my_xlabel.append(label[j])

for i in range(len(my_xlabel)):
    my_xAxis.append(x[0] + i*len(SnoopType)*width + float(int(i / len(Standrad_order))) * 0.2)

for i in range(len(job_list)):
    plt.text(x[0] + 0.4 + i, 100000000, job_list[i], fontsize=14, color='black')
#my_xAxis = np.arange(0- (total_width - width) / 2,len(job_list)- (total_width - width) / 2, (1 / len(Standrad_order)))
#print(my_xlabel)
#print(my_xAxis)
plt.xticks(my_xAxis, my_xlabel,rotation=20, ha='right') 
plt.legend(ncol = 5)
plt.savefig(gem5_root+'picture/StandardSnoop.pdf', bbox_inches='tight')