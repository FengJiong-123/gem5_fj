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
    num_rows = 32
    num_cols = 32


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
        router_list = [  8,  16, 24, #40, 41, 42, 43, 44, 45, 46, 47, 56, 57, 58, 59, 60, 61, 62, 63,
                        #72, 73, 74, 75, 76, 77, 78, 79, 88, 89, 90, 91, 92, 93, 94, 95,104,105,106,107,108,109,110,111,120,121,122,123,124,125,126,127,
                       #128,129,130,131,132,133,134,135,144,145,146,147,148,149,150,151,160,161,162,163,164,165,166,167,176,177,178,179,180,181,182,183,
                       256,264,272,280,#224,225,226,227,228,229,230,231,240,241,242,243,244,245,246,247,
                       #136,137,138,139,140,141,142,143,152,153,154,155,156,157,158,159,168,169,170,171,172,173,174,175,184,185,186,187,188,189,190,191,
                       512,520,528,536,
                       768,776,784,792]

class CHI_HNF(CHI_config.CHI_HNF):
    class NoC_Params(CHI_config.CHI_HNF.NoC_Params):
        #router_list = [0, 1, 2, 3, 16, 17, 18, 19, 32, 33, 34, 35, 48, 49, 50, 51]
        #router_list = [  0,  1,  2,  3,  4,  5,  6,  7, 16, 17, 18, 19, 20, 21, 22, 23, 32, 33, 34, 35, 36, 37, 38, 39, 48, 49, 50, 51, 52, 53, 54, 55,
                        #64, 65, 66, 67, 68, 69, 70, 71, 80, 81, 82, 83, 84, 85, 86, 87, 96, 97, 98, 99,100,101,102,103,112,113,114,115,116,117,118,119]
        router_list = [  0,  2,  4,  6, 33, 35, 37, 39, 64, 66, 68, 70, 97, 99,101,103,
                       128,130,132,134,161,163,165,167,192,194,196,198,225,227,229,231]


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
