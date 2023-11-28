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
        router_list = [  0,  1,  2,  3,
                        32, 33, 34, 35,
                        64, 65, 66, 67,
                        96, 97, 98, 99]
                        

class CHI_RNV(CHI_config.CHI_RNV):
    class NoC_Params(CHI_config.CHI_RNV.NoC_Params):
        router_list = [  8, 9, 10, 11,     16, 17, 18, 19,     24, 25, 26, 27, 
                        40, 41,42, 43,     48, 49, 50, 51,     56, 57, 58, 59,
                        72, 73, 74, 75,    80, 81, 82, 83,     88, 89, 90, 91,
                       104,105,106,107,   112,113,114,115,    120,121,122,123,

                       256,257,258,259,   264,265,266,267,    272,273,274,275,   280,281,282,283,
                       288,289,290,291,   296,297,298,299,    304,305,306,307,   312,313,314,315,
                       320,321,322,323,   328,329,330,331,    336,337,338,339,   344,345,346,347,
                       352,353,354,355,   360,361,362,363,    368,369,370,371,   376,377,378,379,

                       512,513,514,515,   520,521,522,523,    528,529,530,531,   536,537,538,539,
                       544,545,546,547,   552,553,554,555,    560,561,562,563,   568,569,570,571,
                       576,577,578,579,   584,585,586,587,    592,593,594,595,   600,601,602,603,

                       768,769,770,771,   776,777,778,779,    784,785,786,787,   792,793,794,795,
                       800,801,802,803,   808,809,810,811,    816,817,818,819,   824,825,826,827,
                       832,833,834,835,   840,841,842,843,    848,849,850,851,   856,857,858,859,
                       864,865,866,867,   872,873,874,875,    880,881,882,883,   888,889,890,891]

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
