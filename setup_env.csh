echo '  Start set env  '
echo ''

setenv redirect /hpc/users/HKUST-GZ/huanglab/fj/gcc-linux-arm/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/
setenv redirect_lib /hpc/users/HKUST-GZ/huanglab/fj/gcc-linux-arm/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/lib
setenv redirect_lib64 /hpc/users/HKUST-GZ/huanglab/fj/gcc-linux-arm/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/lib64
setenv redirect_usr_lib64 /hpc/users/HKUST-GZ/huanglab/fj/gcc-linux-arm/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/usr/lib64

alias toGem5 'cd /hpc/users/HKUST-GZ/huanglab/fj/gem5Try/gem5'
echo 'toGem5 = cd /hpc/users/HKUST-GZ/huanglab/fj/gem5Try/gem5'
echo ''

alias model_arm_build 'scons build/ARM_CHI/gem5.opt --default=ARM PROTOCOL=CHI SLICC_HTML=True -j32'
echo 'model_arm_build = scons build/ARM_CHI/gem5.opt --default=ARM PROTOCOL=CHI SLICC_HTML=True -j32'
echo ''

alias model_x86_build 'scons build/X86_CHI/gem5.opt --default=X86 PROTOCOL=CHI SLICC_HTML=True -j16'
echo 'model_x86_build = scons build/X86_CHI/gem5.opt --default=X86 PROTOCOL=CHI SLICC_HTML=True -j16'
echo ''

alias build_bw_mem 'cd tests/test-progs/bw_memrdwr/src/ && ./build_arm.sh && ./build_x86.sh && cd -'
echo 'build_bw_mem = cd tests/test-progs/bw_memrdwr/src/ && ./build_arm.sh && ./build_x86.sh && cd -'
echo ''

alias build_bw_mem_gsr 'cd tests/test-progs/bw_mem_gsr/src/ && ./build_arm.sh && ./build_x86.sh && cd -'
echo 'build_bw_mem_gsr = cd tests/test-progs/bw_mem_gsr/src/ && ./build_arm.sh && ./build_x86.sh && cd -'
echo ''

alias build_threadplus 'cd tests/test-progs/threadplus/src/ && ./build_arm.sh && ./build_x86.sh && cd -'
echo 'build_threadplus = cd tests/test-progs/threadplus/src/ && ./build_arm.sh && ./build_x86.sh && cd -'
echo ''

alias model_arm_run_bw_mem 'build/ARM_CHI/gem5.opt -d bw_mem configs/deprecated/example/se.py -n 64 --l2cache --num-l2caches 64 --num-l3caches 16 --l1i_size 65536 --l1i_assoc 4 --l1d_size 65534 --l1d_assoc 4 --l2_size 2097152 --l2_assoc 8 --l3_size 2097152 --l3_assoc 8 --num-dirs 4 --interp-dir=/hpc2hdd/home/jfeng293/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/ --redirects /lib=/hpc2hdd/home/jfeng293/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/lib --redirects /lib64=/hpc2hdd/home/jfeng293/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/lib64 --redirects /usr/lib64=/hpc2hdd/home/jfeng293/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/usr/lib64 --cmd tests/test-progs/bw_memrdwr/src/threads-arm --options='1M 1 1 rd' --ruby --topology=CustomMesh --chi-config=configs/example/noc_config/16x16_v2.py --network=garnet'
echo 'model_arm_run_bw_mem = '
echo '                      build/ARM_CHI/gem5.opt -d bw_mem configs/deprecated/example/se.py -n 64 --l2cache --num-l2caches 64 --num-l3caches 16 --l1i_size 65536 --l1i_assoc 4 --l1d_size 65534 --l1d_assoc 4 --l2_size 2097152 --l2_assoc 8 --l3_size 2097152 --l3_assoc 8 --num-dirs 4 --interp-dir=/hpc2hdd/home/jfeng293/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/ --redirects /lib=/hpc2hdd/home/jfeng293/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/lib --redirects /lib64=/hpc2hdd/home/jfeng293/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/lib64 --redirects /usr/lib64=/hpc2hdd/home/jfeng293/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/usr/lib64 --cmd tests/test-progs/bw_memrdwr/src/threads-arm --options='1M 1 1 rd' --ruby --topology=CustomMesh --chi-config=configs/example/noc_config/16x16_v2.py --network=garnet'
echo ''

alias model_arm_run_bwmem_gsr 'build/ARM_CHI/gem5.opt -d bw_mem_gsr --debug-flag=RubySlicc --debug-file=debug.txt --debug-start=8000 --debug-end=10000 configs/deprecated/example/se.py -n 64 --l2cache --num-l2caches 64 --num-l3caches 16 --l1i_size 65536 --l1i_assoc 4 --l1d_size 65534 --l1d_assoc 4 --l2_size 2097152 --l2_assoc 8 --l3_size 2097152 --l3_assoc 8 --num-dirs 4 --interp-dir=/hpc/users/HKUST-GZ/huanglab/fj/gcc-linux-arm/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/ --redirects /lib=/hpc/users/HKUST-GZ/huanglab/fj/gcc-linux-arm/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/lib --redirects /lib64=/hpc/users/HKUST-GZ/huanglab/fj/gcc-linux-arm/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/lib64 --redirects /usr/lib64=/hpc/users/HKUST-GZ/huanglab/fj/gcc-linux-arm/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/usr/lib64 --cmd tests/test-progs/bw_mem_gsr/src/threads-arm --ruby --topology=CustomMesh --chi-config=configs/example/noc_config/16x16_v2.py --network=garnet'
echo 'model_arm_run_bwmem_gsr = '
echo '                         build/ARM_CHI/gem5.opt -d bw_mem_gsr --debug-flag=RubySlicc --debug-file=debug.txt --debug-start=8000 --debug-end=10000 configs/deprecated/example/se.py -n 64 --l2cache --num-l2caches 64 --num-l3caches 16 --l1i_size 65536 --l1i_assoc 4 --l1d_size 65534 --l1d_assoc 4 --l2_size 2097152 --l2_assoc 8 --l3_size 2097152 --l3_assoc 8 --num-dirs 4 --interp-dir=/hpc/users/HKUST-GZ/huanglab/fj/gcc-linux-arm/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/ --redirects /lib=/hpc/users/HKUST-GZ/huanglab/fj/gcc-linux-arm/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/lib --redirects /lib64=/hpc/users/HKUST-GZ/huanglab/fj/gcc-linux-arm/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/lib64 --redirects /usr/lib64=/hpc/users/HKUST-GZ/huanglab/fj/gcc-linux-arm/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/usr/lib64 --cmd tests/test-progs/bw_mem_gsr/src/threads-arm --ruby --topology=CustomMesh --chi-config=configs/example/noc_config/16x16_v2.py --network=garnet'
echo ''

alias model_x86_run_bw_mem 'build/X86_CHI/gem5.opt configs/deprecated/example/se.py -n 4 --cmd ./tests/test-progs/bw_memrdwr/src/threads --ruby  --topology=CustomMesh --chi-config=configs/example/noc_config/2x4.py --network=garnet'
echo 'model_x86_run_bw_mem = '
echo '            build/X86_CHI/gem5.opt configs/deprecated/example/se.py -n 4 --cmd ./tests/test-progs/bw_memrdwr/src/threads --ruby  --topology=CustomMesh --chi-config=configs/example/noc_config/2x4.py --network=garnet'

alias model_run_arm_spec '/hpc2hdd/home/jfeng293/gem5/build/ARM_CHI/gem5.opt -d /hpc2hdd/home/jfeng293/gem5/debug /hpc2hdd/home/jfeng293/gem5/configs/deprecated/example/se.py -n 1 --l2cache --num-l2caches 1 --num-l3caches 16 --l1i_size 65536 --l1i_assoc 4 --l1d_size 65534 --l1d_assoc 4 --l2_size 2097152 --l2_assoc 8 --l3_size 2097152 --l3_assoc 8 --num-dirs 4 --interp-dir=/hpc2hdd/home/jfeng293/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/ --redirects /lib=/hpc2hdd/home/jfeng293/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/lib --redirects /lib64=/hpc2hdd/home/jfeng293/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/lib64 --redirects /usr/lib64=/hpc2hdd/home/jfeng293/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/usr/lib64 --cmd '../../build/build_base_mytest-64.0000/perlbench_r' --options='-I./lib checkspam.pl 2500 5 25 11 150 1 1 1 1' --ruby --topology=CustomMesh --chi-config=/hpc2hdd/home/jfeng293/gem5/configs/example/noc_config/16x16_v2.py --network=garnet'

echo 'Basic take checkpoints: '
echo 'build/ARM_MOESI/gem5.opt -d bw_mem --debug-flag=RubyCacheTrace --debug-file=debug.txt configs/deprecated/example/se.py -n 1 --interp-dir=/hpc2hdd/home/jfeng293/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/ --redirects /lib=/hpc2hdd/home/jfeng293/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/lib --redirects /lib64=/hpc2hdd/home/jfeng293/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/lib64 --redirects /usr/lib64=/hpc2hdd/home/jfeng293/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/usr/lib64 --cmd tests/test-progs/bw_memrdwr/src/threads-arm --options='1M 1 1 rd' --take-checkpoints 1000000000,1000000000'

echo 'take simpoint checkpoint:  '
echo '1. Initiate and capture .bb file for simpoint.'
echo 'build/ARM_MOESI/gem5.opt -d bw_mem --debug-flag=RubyCacheTrace --debug-file=debug.txt configs/deprecated/example/se.py -n 1 --interp-dir=/hpc2hdd/home/jfeng293/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/ --redirects /lib=/hpc2hdd/home/jfeng293/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/lib --redirects /lib64=/hpc2hdd/home/jfeng293/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/lib64 --redirects /usr/lib64=/hpc2hdd/home/jfeng293/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/usr/lib64 --cmd tests/test-progs/bw_memrdwr/src/threads-arm --options='16M 1 1 rd' --simpoint-profile --simpoint-interval 100000 --cpu-type=NonCachingSimpleCPU'
echo '2. execuate simpoint .bb file'
echo './simpoint -loadFVFile /hpc2hdd/home/jfeng293/gem5/bw_mem/simpoint.bb.gz -maxK 30 -saveSimpoints /hpc2hdd/home/jfeng293/gem5/bw_mem/bw_mem.simpoints -saveSimpointWeights /hpc2hdd/home/jfeng293/gem5/bw_mem/bw_mem.weights -inputVectorsGzipped'
echo '3. generate checkpoint'
echo 'build/ARM_MOESI/gem5.opt -d bw_mem --debug-flag=RubyCacheTrace --debug-file=debug.txt configs/deprecated/example/se.py -n 1 --interp-dir=/hpc2hdd/home/jfeng293/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/ --redirects /lib=/hpc2hdd/home/jfeng293/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/lib --redirects /lib64=/hpc2hdd/home/jfeng293/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/lib64 --redirects /usr/lib64=/hpc2hdd/home/jfeng293/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu/aarch64-none-linux-gnu/libc/usr/lib64 --cmd tests/test-progs/bw_memrdwr/src/threads-arm --options='16M 1 1 rd' --take-simpoint-checkpoint=bw_mem/bw_mem.simpoints,bw_mem/bw_mem.weights,300000,10000'
echo 'Then the checkpoint generate successfully'

build/X86_MOESI/gem5.opt -d bw_mem_x86 configs/deprecated/example/se.py -n 1  --cmd tests/test-progs/bw_memrdwr/src/threads --options='1M 1 1 rd' --take-checkpoints=10000000,10000000
build/X86_MOESI/gem5.opt -d bw_mem_x86 configs/deprecated/example/se.py -n 1  --cmd tests/test-progs/bw_memrdwr/src/threads --options='1M 1 1 rd' --checkpoint-dir=bw_mem_x86 -r 5
build/X86_CHI/gem5.opt -d bw_mem_x86 configs/deprecated/example/se.py -n 1 --l2cache --num-l2caches 64 --num-l3caches 16 --l1i_size 65536 --l1i_assoc 4  --l1d_size 65534 --l1d_assoc 4 --l2_size 2097152 --l2_assoc 8 --l3_size 2097152 --l3_assoc 8 --num-dirs 4 --ruby --topology=CustomMesh --chi-config=configs/example/noc_config/16x16_v2.py --network=garnet --cmd tests/test-progs/bw_memrdwr/src/threads --options='1M 1 1 rd' --checkpoint-dir=bw_mem_x86 -r 5

/hpc2hdd/home/jfeng293/gem5/build/X86_CHI/gem5.opt -d /hpc2hdd/home/jfeng293/gem5/debug/x264_r_1_init/ /hpc2hdd/home/jfeng293/gem5/configs/deprecated/example/se.py -n 1 --l2cache --num-l2caches 64 --num-l3caches 16 --l1i_size 65536 --l1i_assoc 4  --l1d_size 65534 --l1d_assoc 4 --l2_size 2097152 --l2_assoc 8 --l3_size 2097152 --l3_assoc 8 --num-dirs 4 --ruby --topology=CustomMesh --chi-config=/hpc2hdd/home/jfeng293/gem5/configs/example/noc_config/16x16_v2.py --network=garnet --cmd ../../build/build_base_mytest-m64.0000/x264_r '--options=--pass 1 --stats x264_stats.log --bitrate 1000 --frames 1000 -o BuckBunny_New.264 BuckBunny.264 1280x720' --restore-simpoint-checkpoint --checkpoint-dir=/hpc2hdd/home/jfeng293/gem5/debug/x264_r_1_init -r 2 --mem-size=4GB --cpu-type=O3CPU

/hpc2hdd/home/jfeng293/gem5/build/X86_CHI/gem5.opt -d /hpc2hdd/home/jfeng293/gem5/debug/xz_r_2_init \
                                                      /hpc2hdd/home/jfeng293/gem5/configs/deprecated/example/se.py -n 1 \
                                                      --mem-size=4GB --l2cache --num-l2caches 1 --l1i_size 65536  \
                                                      --l1i_assoc 4 --l1d_size 65534 --l1d_assoc 4 --l2_size 2097152 --l2_assoc 8 \
                                                      --num-l3caches 16 --l3_size 2097152 --l3_assoc 8 --num-dirs 4 \
                                                      --num-rnv 3 --cluster_num 1  --dir_bits 20 --dir_assoc_bit 1 \
                                                      --ruby --topology=CustomMesh --chi-config=/hpc2hdd/home/jfeng293/gem5/configs/example/noc_config/16x16_v2.py --network=garnet \
                                                      --cmd '../../build/build_base_mytest-m64.0000/xz_r' --options='cpu2006docs.tar.xz 250 055ce243071129412e9dd0b3b69a21654033a9b723d874b2015c774fac1553d9713be561ca86f74e4f16f22e664fc17a79f30caa5ad2c04fbc447549c2810fae 23047774 23513385 6e' \
                                                      --restore-simpoint-checkpoint --checkpoint-dir=/hpc2hdd/home/jfeng293/gem5/debug/xz_r_2_init -r 12 --cpu-type=O3CPU

build/X86_CHI/gem5.opt -d bw_mem_x86 --debug-flag=RubySlicc --debug-file=debug.txt --debug-start=20000000 --debug-end=30000000 configs/deprecated/example/se.py -n 1 --l2cache --num-l2caches 1 --num-l3caches 16 --num-rnv 3 --l1i_size 65536 --l1i_assoc 4  --l1d_size 65534 --l1d_assoc 4 --l2_size 2097152 --l2_assoc 8 --l3_size 2097152 --l3_assoc 8 --num-dirs 4 --ruby --topology=CustomMesh --chi-config=configs/example/noc_config/2x4.py --network=garnet --cmd tests/test-progs/bw_memrdwr/src/threads --options='1M 1 1 rd' --cpu-type=O3CPU