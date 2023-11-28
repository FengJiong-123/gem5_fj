import os
import sys
import time

job_file = 'bw_mem_submit_11_10'
gem5_dir = os.getcwd()
Core_num = {64}
Assoc = {3}
Test_case = {'rd', 'wr'}
cluster_num = {1, 4}

#mkdir
if not os.path.exists(job_file):
    os.system('mkdir '+ job_file)
else:
    os.system('rm -rf '+ job_file)
    os.system('mkdir '+ job_file)

for i in range(14,16):

    for c in Core_num:

        for a in Assoc:

            if i < 12 and a > 0:
                continue

            for case in Test_case:

                if case == 'wr' and c == 4:
                    continue

                for C_num in cluster_num:

                    for g in range(0,2):

                        if (g == 1) and (C_num == 1):
                            continue

                        script_file_name = job_file + '/bw_mem_'+str(i) +str(c)+str(a)+case+str(C_num)+str(g)+'.sh'
                        print('Generate bw_mem test with : '+ str(i)+str(c)+str(a)+case+str(C_num)+str(g))
                        script_file = open(script_file_name, 'w')

                        script_file.write('#!/bin/bash\n')
                        script_file.write('#SBATCH -p i64m512u\n')
                        script_file.write('#SBATCH -J ' + str(i)+str(c)+str(a)+case +str(C_num)+str(g)+'\n')
                        script_file.write('#SBATCH --ntasks-per-node=6\n')
                        script_file.write('#SBATCH --mem=48000\n')
                        script_file.write('#SBATCH  -n 6\n')
                        script_file.write('#SBATCH -o '+job_file+'/bw_'+ str(i)+str(c)+str(a)+case+str(C_num)+str(g)+'.%j.out\n')
                        script_file.write('#SBATCH -e '+job_file+'/bw_'+ str(i)+str(c)+str(a)+case+str(C_num)+str(g)+'.%j.err\n\n\n')

                        script_file.write(gem5_dir+"/build/X86_CHI/gem5.opt -d bw_mem_sub/dir_" + str(i)+str(c)+str(a)+case+str(C_num)+str(g))
                        script_file.write(" "+gem5_dir+"/configs/deprecated/example/se.py -n "+str(c))
                        script_file.write(" --mem-size=4GB --l2cache --num-l2caches "+str(c)+" --l1i_size 64kB --l1i_assoc 4 --l1d_size 64kB --l1d_assoc 4 --l2_size 1MB --l2_assoc 8 --num-l3caches 32")
                        script_file.write(" --l3_size 1MB --l3_assoc 8 --num-dirs 8 --num-rnv "+str(c*3)+" --cluster_num "+str(C_num)+" --enable_gsr "+str(g)+"  --dir_bits "+ str(i))
                        script_file.write(" --dir_assoc "+str(a)+"  --ruby --topology=CustomMesh --chi-config=/hpc2hdd/home/jfeng293/gem5/configs/example/noc_config/16x16_"+str(c)+"c_"+str(c*3)+"vc.py --network=garnet")
                        script_file.write(" --cmd /hpc2hdd/home/jfeng293/gem5/tests/test-progs/bw_memrdwr/src/threads --options='64M "+str(c)+" 1 rd' --cpu-type=O3CPU -m 13337525300000")
                        script_file.close()
                        os.system('chmod 777 '+ script_file_name)

                        
                        os.chdir(gem5_dir + '/' + job_file)
                        os.system('sbatch '+ 'bw_mem_'+str(i)+str(c)+str(a)+case+str(C_num)+str(g)+ '.sh')
                        os.chdir(gem5_dir)
                        time.sleep(5)
    