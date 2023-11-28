# Copyright (c) 2021 ARM Limited
# All rights reserved.
#
# This topology will be used to simu cluster

from ruby import CHI_config

#
# 0 --- 1 ... 14 --- 15
# .                   .
# .                   .
# 240--241...254 --- 255
#
# Default parameter are configs/ruby/CHI_config.py
#
class NoC_Params(CHI_config.NoC_Params):
    num_rows = 16
    num_cols = 16


# Specialization of nodes to define bindings for each CHI node type
# needed by CustomMesh.
# The default types are defined in CHI_Node and their derivatives in
# configs/ruby/CHI_config.py


class CHI_RNF(CHI_config.CHI_RNF):
    class NoC_Params(CHI_config.CHI_RNF.NoC_Params):
        #router_list = [28, 29, 30, 31, 24, 25, 26, 27, 20, 21, 22, 23, 16, 17, 18, 19, 12, 13, 14, 15, 8, 9, 10, 11, 4, 5, 6, 7, 0, 1, 2, 3]
        router_list = [  0]
                        #64, 65, 66, 67, 68, 69, 70, 71, 80, 81, 82, 83, 84, 85, 86, 87, 96, 97, 98, 99,100,101,102,103,112,113,114,115,116,117,118,119]
                        #12, 13, 14, 15, 28, 29, 30, 31, 44, 45, 46, 47, 60, 61, 62, 63, 
                       #192,193,194,195,208,209,210,211,224,225,226,227,240,241,242,243, 
                       #204,205,206,207,220,221,222,223,236,237,238,239,252,253,254,255]

class CHI_RNV(CHI_config.CHI_RNV):
    class NoC_Params(CHI_config.CHI_RNV.NoC_Params):
        router_list = [  1, 16, 17]

class CHI_HNF(CHI_config.CHI_HNF):
    class NoC_Params(CHI_config.CHI_HNF.NoC_Params):
        #router_list = [0, 1, 2, 3, 16, 17, 18, 19, 32, 33, 34, 35, 48, 49, 50, 51]
        #router_list = [  0,  1,  2,  3,  4,  5,  6,  7, 16, 17, 18, 19, 20, 21, 22, 23, 32, 33, 34, 35, 36, 37, 38, 39, 48, 49, 50, 51, 52, 53, 54, 55,
                        #64, 65, 66, 67, 68, 69, 70, 71, 80, 81, 82, 83, 84, 85, 86, 87, 96, 97, 98, 99,100,101,102,103,112,113,114,115,116,117,118,119]
        router_list = [  0,  2,  4,  6, 17, 19, 21, 23, 32, 34, 36, 38, 49, 51, 53, 55,
                        64, 66, 68, 70, 81, 83, 85, 87, 96, 98,100,102,113,115,117,119]


class CHI_MN(CHI_config.CHI_MN):
    class NoC_Params(CHI_config.CHI_MN.NoC_Params):
        router_list = [4]


class CHI_SNF_MainMem(CHI_config.CHI_SNF_MainMem):
    class NoC_Params(CHI_config.CHI_SNF_MainMem.NoC_Params):
        router_list = [0, 16, 32, 48, 64, 80, 96, 112]


class CHI_SNF_BootMem(CHI_config.CHI_SNF_BootMem):
    class NoC_Params(CHI_config.CHI_SNF_BootMem.NoC_Params):
        router_list = [28, 24, 20, 16, 12, 8, 4, 0]


class CHI_RNI_DMA(CHI_config.CHI_RNI_DMA):
    class NoC_Params(CHI_config.CHI_RNI_DMA.NoC_Params):
        router_list = [7]


class CHI_RNI_IO(CHI_config.CHI_RNI_IO):
    class NoC_Params(CHI_config.CHI_RNI_IO.NoC_Params):
        router_list = [7]
