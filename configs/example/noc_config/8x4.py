# Copyright (c) 2021 ARM Limited
# All rights reserved.
#
# This topology refer to the topology of ptg yitian710 single die topology

from ruby import CHI_config

# CustomMesh parameters for a 10x4 mesh. Routers will have the following layout:
#
# 0 --- 1 --- 2 --- 3
# |     |     |     |
# 4 --- 5 --- 6 --- 7
# |     |     |     |
# 8 --- 9 --- 10 -- 11
# |     |     |     |
# 12 -- 13 -- 14 -- 15
# |     |     |     |
# 16 -- 17 -- 18 -- 19
# |     |     |     |
# 20 -- 21 -- 22 -- 23
# |     |     |     |
# 24 -- 25 -- 26 -- 27
# |     |     |     |
# 28 -- 29 -- 30 -- 31
#
# Default parameter are configs/ruby/CHI_config.py
#
class NoC_Params(CHI_config.NoC_Params):
    num_rows = 8
    num_cols = 4


# Specialization of nodes to define bindings for each CHI node type
# needed by CustomMesh.
# The default types are defined in CHI_Node and their derivatives in
# configs/ruby/CHI_config.py


class CHI_RNF(CHI_config.CHI_RNF):
    class NoC_Params(CHI_config.CHI_RNF.NoC_Params):
        #router_list = [28, 29, 30, 31, 24, 25, 26, 27, 20, 21, 22, 23, 16, 17, 18, 19, 12, 13, 14, 15, 8, 9, 10, 11, 4, 5, 6, 7, 0, 1, 2, 3]
        router_list = [28, 29, 30, 31, 24, 25, 26, 27, 20, 21, 22, 23, 16, 17, 18, 19]


class CHI_HNF(CHI_config.CHI_HNF):
    class NoC_Params(CHI_config.CHI_HNF.NoC_Params):
        router_list = [28, 29, 30, 31, 24, 25, 26, 27, 20, 21, 22, 23, 16, 17, 18, 19, 12, 13, 14, 15, 8, 9, 10, 11, 4, 5, 6, 7, 0, 1, 2, 3]


class CHI_MN(CHI_config.CHI_MN):
    class NoC_Params(CHI_config.CHI_MN.NoC_Params):
        router_list = [4]


class CHI_SNF_MainMem(CHI_config.CHI_SNF_MainMem):
    class NoC_Params(CHI_config.CHI_SNF_MainMem.NoC_Params):
        router_list = [28, 24, 20, 16, 12, 8, 4, 0]


class CHI_SNF_BootMem(CHI_config.CHI_SNF_BootMem):
    class NoC_Params(CHI_config.CHI_SNF_BootMem.NoC_Params):
        router_list = [28, 24, 20, 16, 12, 8, 4, 0]


class CHI_RNI_DMA(CHI_config.CHI_RNI_DMA):
    class NoC_Params(CHI_config.CHI_RNI_DMA.NoC_Params):
        router_list = [7]


class CHI_RNI_IO(CHI_config.CHI_RNI_IO):
    class NoC_Params(CHI_config.CHI_RNI_IO.NoC_Params):
        router_list = [7]
