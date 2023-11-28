import os
import sys
import time

gem5_root = '/hpc2hdd/home/jfeng293/gem5_dir_fass/'
job_list = {#'cachebw',
            #'bfs',
            #'kmeans',
            'lud'
            #'nw'
            #'hotspot3D',
            #'hotspot',
            #'srad',
            #'pathfinder'
            }
#Cores = {4, 16}
if len(sys.argv) < 2:
    assert(0)

Cores = sys.argv[1]
Clusters = {4, 16}
GSR = {0, 1}
#GSR = {1}
RNVs = {0, 4, 12, 28, 60}
#RNVs = {0, 16, 48} #for 16 cores
#RNVs = {12}


job_file = 'Multithread_all_11_22'

#mkdir
if not os.path.exists(job_file):
    os.system('mkdir '+ job_file)
    os.system('rm -f '+ job_file + '/' + '*err')
    os.system('rm -f '+ job_file + '/' + '*out')

# generate submittion script
for job in job_list:
    for cluster in Clusters:

        for rnv in RNVs:

            if cluster == 1 and rnv != 0:
                continue

            #if cluster == 4 and (rnv == 28 or rnv == 60):
            #    continue

            if cluster == 16 and (rnv == 0 or rnv == 4):
                continue

            for gsr in GSR:

                if gsr == 1:
                    #if cluster == 4:
                    #    if rnv != 4:
                    #        continue
                    #if cluster == 16:
                    #    if not (rnv == 28 or rnv == 12):
                    #        continue
                    if cluster == 1:
                        continue

                #if job == 'pathfinder':
                #    if not rnv == 0:
                #        continue

                #if job == 'hotspot':
                #    if not rnv == 16 or not gsr == 1:
                #        continue      

                script_file_name = job_file + '/' + job + str(cluster)+ str(rnv) + str(gsr) + Cores +'.sh'

                print('Generate submittion script', job, cluster, rnv, gsr, Cores)
                script_file = open(script_file_name, 'w')


                script_file.write('#!/bin/bash\n')
                script_file.write('#SBATCH -J ' +str(cluster)+str(rnv) +str(gsr) +Cores+ job +'\n')
                if not rnv == 28 or not rnv == 60 or not rnv == 48:
                    script_file.write('#SBATCH -p i64m512u\n')
                    script_file.write('#SBATCH --ntasks-per-node=3\n')
                    script_file.write('#SBATCH  -n 2\n')
                    script_file.write('#SBATCH  --mem 16000\n')
                else:
                    script_file.write('#SBATCH -p i96m3tu\n')
                    script_file.write('#SBATCH --ntasks-per-node=10\n')
                    script_file.write('#SBATCH  -n 10\n')
                    script_file.write('#SBATCH  --mem 80000\n')
                script_file.write('#SBATCH -o '+gem5_root+job_file+ '/'+job +str(cluster)+str(rnv) +str(gsr) +Cores +'.%j.out\n')
                script_file.write('#SBATCH -e '+gem5_root+job_file+ '/'+job +str(cluster)+str(rnv) +str(gsr) +Cores +'.%j.err\n\n\n')

                script_file.write('echo $(date +%F/%T)\n')

                if job == 'cachebw':
                    cmd  = "'/hpc2hdd/home/jfeng293/gem5_dir_fass/nuca-bench/benchmarks/bin/cachebw.exe'"
                    opt  = "'524288 1 1 1 1 "+Cores+"'"
                elif job == 'bfs':
                    cmd  = "'/hpc2hdd/home/jfeng293/gem5_dir_fass/nuca-bench/benchmarks/bin/rodinia/bfs.exe'"
                    opt  = "'"+Cores+" /hpc2hdd/home/jfeng293/gem5_dir_fass/nuca-bench/benchmarks/rodinia/data/bfs/graph65536.txt.data'"
                elif job == 'btree':
                    cmd  = "'/hpc2hdd/home/jfeng293/gem5_dir_fass/nuca-bench/benchmarks/bin/rodinia/btree.exe'"
                    opt  = "'cores "+Cores+" fake'"
                elif job == 'cfd':
                    cmd  = "'/hpc2hdd/home/jfeng293/gem5_dir_fass/nuca-bench/benchmarks/bin/rodinia/euler3d_cpu_double.exe'"
                    opt  = "'/hpc2hdd/home/jfeng293/gem5_dir_fass/nuca-bench/benchmarks/rodinia/data/cfd/fvcorr.domn.097K.data "+Cores+" 1'"
                elif job == 'kmeans':
                    cmd  = "'/hpc2hdd/home/jfeng293/gem5_dir_fass/nuca-bench/benchmarks/bin/rodinia/kmeans.exe'"
                    opt  = "'-i /hpc2hdd/home/jfeng293/gem5_dir_fass/nuca-bench/benchmarks/rodinia/data/kmeans/100.data -b 1 -n "+Cores+"'"
                elif job == 'lud':
                    cmd  = "'/hpc2hdd/home/jfeng293/gem5_dir_fass/nuca-bench/benchmarks/bin/rodinia/lud.exe'"
                    opt  = "'-n "+Cores+" -s 512'"
                elif job == 'nw':
                    cmd  = "'/hpc2hdd/home/jfeng293/gem5_dir_fass/nuca-bench/benchmarks/bin/rodinia/needle.exe'"
                    opt  = "'2048 10 "+Cores+"'"
                elif job == 'pathfinder':
                    cmd  = "'/hpc2hdd/home/jfeng293/gem5_dir_fass/nuca-bench/benchmarks/bin/rodinia/pathfinder.exe'"
                    opt  = "'1500000 8 "+Cores+"'"

                elif job == 'hotspot3D':
                    cmd  = "'/hpc2hdd/home/jfeng293/gem5_dir_fass/nuca-bench/benchmarks/bin/rodinia/hotspot3D.exe'"
                    opt  = "'512 8 8 "+Cores+" /hpc2hdd/home/jfeng293/gem5_dir_fass/nuca-bench/benchmarks/rodinia/data/hotspot/power_512x8 /hpc2hdd/home/jfeng293/gem5_dir_fass/nuca-bench/benchmarks/rodinia/data/hotspot/temp_512x8 /hpc2hdd/home/jfeng293/gem5_dir_fass/nuca-bench/benchmarks/rodinia/data/hotspot/output_512x8.txt'"

                elif job == 'hotspot':
                    cmd  = "'/hpc2hdd/home/jfeng293/gem5_dir_fass/nuca-bench/benchmarks/bin/rodinia/hotspot.exe'"
                    opt  = "'1024 1024 8 "+Cores+" /hpc2hdd/home/jfeng293/gem5_dir_fass/nuca-bench/benchmarks/rodinia/data/hotspot/temp_1024 /hpc2hdd/home/jfeng293/gem5_dir_fass/nuca-bench/benchmarks/rodinia/data/hotspot/power_1024 /hpc2hdd/home/jfeng293/gem5_dir_fass/nuca-bench/benchmarks/rodinia/data/hotspot/output_1024.txt'"

                elif job == 'srad':
                    cmd  = "'/hpc2hdd/home/jfeng293/gem5_dir_fass/nuca-bench/benchmarks/bin/rodinia/srad.exe'"
                    opt  = "'512 2048 0 127 0 127 "+Cores+" 0.5 8'"
                elif job == 'conv3d':
                    cmd  = "'/hpc2hdd/home/jfeng293/gem5_dir_fass/nuca-bench/benchmarks/bin/gem-forge/omp_conv3d2_unroll_xy.exe'"
                    opt  = "'"+Cores+"'"
                elif job == 'mv':
                    cmd  = "'/hpc2hdd/home/jfeng293/gem5_dir_fass/nuca-bench/benchmarks/bin/gem-forge/omp_dense_mv_blk.exe'"
                    opt  = "'"+Cores+"'"
                else:
                    print("Wrong bench!!!"+job)
                    assert(0)

                if Cores == '4':
                    script_file.write(gem5_root + 'build/X86_CHI/gem5.opt -d ' + gem5_root + job_file + '/' + job + '_' + str(cluster)+ str(rnv) + str(gsr) +' ')
                else:
                    script_file.write(gem5_root + 'build/X86_CHI/gem5.opt -d ' + gem5_root + job_file + '/' + job + '_' + str(cluster)+ str(rnv) + str(gsr)+ Cores +' ')
                script_file.write(gem5_root + 'configs/deprecated/example/se.py -n '+Cores+' --mem-size=1GB --l2cache --num-l2caches '+Cores+' ')
                script_file.write(' --num-l3caches 32 --num_rnv '+str(rnv) +' --l1i_size 64kB --l1i_assoc 4 --l1d_size 64kB --l1d_assoc 4 --l2_size 1MB --l2_assoc 8')
                if job == 'nw':
                    script_file.write(' --l3_size 1MB --l3_assoc 8 --dir_bits 18 --dir_assoc 5 --cluster_num '+str(cluster)+' --num-dirs 8 --ruby --topology=CustomMesh')
                else:
                    script_file.write(' --l3_size 1MB --l3_assoc 8 --dir_bits 13 --dir_assoc 3 --cluster_num '+str(cluster)+' --num-dirs 8 --ruby --topology=CustomMesh')
                if Cores == '4':
                    if cluster == 4 and rnv == 4:
                        script_file.write(' --chi-config='+gem5_root+'configs/example/noc_config/16x16_4c_4vc_near.py --network=garnet --cpu-type=O3CPU')
                    elif cluster == 16 and rnv == 12:
                        script_file.write(' --chi-config='+gem5_root+'configs/example/noc_config/16x16_4c_12vc_near.py --network=garnet --cpu-type=O3CPU')
                    elif cluster == 16 and rnv == 28:
                        script_file.write(' --chi-config='+gem5_root+'configs/example/noc_config/16x16_4c_28vc_near.py --network=garnet --cpu-type=O3CPU')
                    else:
                        script_file.write(' --chi-config='+gem5_root+'configs/example/noc_config/16x16_4c_12vc.py --network=garnet --cpu-type=O3CPU')
                elif Cores == '16':
                    if rnv == 48:
                        script_file.write(' --chi-config='+gem5_root+'configs/example/noc_config/16x16_16c_48vc.py --network=garnet --cpu-type=O3CPU')
                    else:
                        script_file.write(' --chi-config='+gem5_root+'configs/example/noc_config/16x16_16c_16vc_near.py --network=garnet --cpu-type=O3CPU')
                else:
                    assert(0)

                script_file.write(' --cmd '+ cmd +' --enable_gsr '+str(gsr) +' --options=' + opt + ' -m 9333752530000 --fast-forward=9223372036854775807')

                script_file.write('\n')
                script_file.write('echo $(date +%F/%T)\n')
                script_file.close()
                os.system('chmod 777 '+ script_file_name)
                os.chdir(gem5_root + '/' + job_file)
                os.system('sbatch '+ job + str(cluster)+str(rnv) +str(gsr) +Cores +'.sh')
                os.chdir(gem5_root)
                time.sleep(10)

    #time.sleep(100)


