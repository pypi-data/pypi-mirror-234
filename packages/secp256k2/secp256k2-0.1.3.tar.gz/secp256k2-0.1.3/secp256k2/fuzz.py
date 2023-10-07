import platform
import os
import sys
import ctypes
import math, pickle

# --------------------------------------------------------------------------------------
if 'win' in platform.platform().lower():
    dirPath = os.path.dirname(os.path.realpath(__file__))
    secFile = dirPath + '/_secp256k1.dll'
    if os.path.isfile(secFile):
        dllPath = os.path.realpath(secFile)
        Fuzz = ctypes.CDLL(dllPath)
    else:
        raise ValueError("File {} not found".format(secFile))
# --------------------------------------------------------------------------------------
if 'linux' in platform.platform().lower():
    dir_Path = os.path.dirname(os.path.realpath(__file__))
    secFile = dir_Path + '/_secp256k1.so'
    if os.path.isfile(secFile):
        dllPath = os.path.realpath(secFile)
        Fuzz = ctypes.CDLL(dllPath)
    else:
        raise ValueError("File {} not found".format(secFile))
# --------------------------------------------------------------------------------------
COIN_BTC = 0
# --------------------------------------------------------------------------------------
Fuzz.scalar_multiplication.argtypes = [ctypes.c_char_p, ctypes.c_char_p]  # pvk,ret
# --------------------------------------------------------------------------------------
Fuzz.scalar_multiplications.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]  # pvk,len,ret
# --------------------------------------------------------------------------------------
Fuzz.get_x_to_y.argtypes = [ctypes.c_char_p, ctypes.c_bool, ctypes.c_char_p]  # x,even,ret
# --------------------------------------------------------------------------------------
Fuzz.point_increment.argtypes = [ctypes.c_char_p, ctypes.c_char_p]  # upub,ret
# --------------------------------------------------------------------------------------
Fuzz.point_negation.argtypes = [ctypes.c_char_p, ctypes.c_char_p]  # upub,ret
# --------------------------------------------------------------------------------------
Fuzz.point_doubling.argtypes = [ctypes.c_char_p, ctypes.c_char_p]  # upub,ret
# --------------------------------------------------------------------------------------
Fuzz.privatekey_to_coinaddress.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_bool,
                                           ctypes.c_char_p]  # intcoin,012,comp,pvk
# --------------------------------------------------------------------------------------
Fuzz.privatekey_to_coinaddress.restype = ctypes.c_void_p
# --------------------------------------------------------------------------------------
Fuzz.privatekey_to_address.argtypes = [ctypes.c_int, ctypes.c_bool, ctypes.c_char_p]  # 012,comp,pvk
# --------------------------------------------------------------------------------------
Fuzz.privatekey_to_address.restype = ctypes.c_void_p
# --------------------------------------------------------------------------------------
Fuzz.hash_to_address.argtypes = [ctypes.c_int, ctypes.c_bool, ctypes.c_char_p]  # 012,comp,hash
# --------------------------------------------------------------------------------------
Fuzz.hash_to_address.restype = ctypes.c_void_p
# --------------------------------------------------------------------------------------
Fuzz.pubkey_to_address.argtypes = [ctypes.c_int, ctypes.c_bool, ctypes.c_char_p]  # 012,comp,upub
# --------------------------------------------------------------------------------------
Fuzz.pubkey_to_address.restype = ctypes.c_void_p
# --------------------------------------------------------------------------------------
Fuzz.privatekey_to_h160.argtypes = [ctypes.c_int, ctypes.c_bool, ctypes.c_char_p, ctypes.c_char_p]  # 012,comp,pvk,ret
# --------------------------------------------------------------------------------------
Fuzz.privatekey_loop_h160.argtypes = [ctypes.c_ulonglong, ctypes.c_int, ctypes.c_bool, ctypes.c_char_p,
                                      ctypes.c_char_p]  # num,012,comp,pvk,ret
# --------------------------------------------------------------------------------------
Fuzz.privatekey_loop_h160_sse.argtypes = [ctypes.c_ulonglong, ctypes.c_int, ctypes.c_bool, ctypes.c_char_p,
                                          ctypes.c_char_p]  # num,012,comp,pvk,ret
# --------------------------------------------------------------------------------------
Fuzz.pubkey_to_h160.argtypes = [ctypes.c_int, ctypes.c_bool, ctypes.c_char_p, ctypes.c_char_p]  # 012,comp,upub,ret
# --------------------------------------------------------------------------------------
Fuzz.pbkdf2_hmac_sha512_dll.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int]  # ret, words, len
# --------------------------------------------------------------------------------------
Fuzz.pbkdf2_hmac_sha512_list.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulonglong, ctypes.c_int,
                                         ctypes.c_ulonglong]  # ret,words,len,mnem_size,total
# --------------------------------------------------------------------------------------
Fuzz.pub_endo1.argtypes = [ctypes.c_char_p, ctypes.c_char_p]  # upub,ret
# --------------------------------------------------------------------------------------
Fuzz.pub_endo2.argtypes = [ctypes.c_char_p, ctypes.c_char_p]  # upub,ret
# --------------------------------------------------------------------------------------
Fuzz.b58_encode.argtypes = [ctypes.c_char_p]  # _h
# --------------------------------------------------------------------------------------
Fuzz.b58_encode.restype = ctypes.c_void_p
# --------------------------------------------------------------------------------------
Fuzz.b58_decode.argtypes = [ctypes.c_char_p]  # addr
# --------------------------------------------------------------------------------------
Fuzz.b58_decode.restype = ctypes.c_void_p
# --------------------------------------------------------------------------------------
Fuzz.bech32_address_decode.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p]  # coin,b32_addr,h160
# --------------------------------------------------------------------------------------
Fuzz.get_sha256.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]  # input, len, ret
# --------------------------------------------------------------------------------------
Fuzz.create_baby_table.argtypes = [ctypes.c_ulonglong, ctypes.c_ulonglong, ctypes.c_char_p]  # start,end,ret
# --------------------------------------------------------------------------------------
Fuzz.point_addition.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
Fuzz.point_subtraction.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
# --------------------------------------------------------------------------------------
Fuzz.point_loop_subtraction.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_char_p,
                                        ctypes.c_char_p]
# --------------------------------------------------------------------------------------
Fuzz.point_loop_addition.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_char_p,
                                     ctypes.c_char_p]
# --------------------------------------------------------------------------------------
Fuzz.point_vector_addition.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_char_p,
                                       ctypes.c_char_p]
# --------------------------------------------------------------------------------------
Fuzz.point_sequential_increment_P2.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_char_p]  # num,upub1,ret
# --------------------------------------------------------------------------------------
Fuzz.point_sequential_increment_P2_mcpu.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_int,
                                                    ctypes.c_char_p]  # num,upub1,mcpu,ret
# --------------------------------------------------------------------------------------
Fuzz.point_sequential_increment.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_char_p]  # num,upub1,ret
# --------------------------------------------------------------------------------------
Fuzz.point_sequential_decrement.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_char_p]  # num,upub1,ret
# --------------------------------------------------------------------------------------
Fuzz.pubkeyxy_to_ETH_address.argtypes = [ctypes.c_char_p]  # upub_xy
Fuzz.pubkeyxy_to_ETH_address.restype = ctypes.c_void_p
# --------------------------------------------------------------------------------------
Fuzz.pubkeyxy_to_ETH_address_bytes.argtypes = [ctypes.c_char_p, ctypes.c_char_p]  # upub_xy, ret
# --------------------------------------------------------------------------------------
Fuzz.privatekey_to_ETH_address.argtypes = [ctypes.c_char_p]  # pvk
Fuzz.privatekey_to_ETH_address.restype = ctypes.c_void_p
# --------------------------------------------------------------------------------------
Fuzz.privatekey_to_ETH_address_bytes.argtypes = [ctypes.c_char_p, ctypes.c_char_p]  # pvk, ret
# --------------------------------------------------------------------------------------
Fuzz.privatekey_group_to_ETH_address.argtypes = [ctypes.c_char_p, ctypes.c_int]  # pvk, m
Fuzz.privatekey_group_to_ETH_address.restype = ctypes.c_void_p
# --------------------------------------------------------------------------------------
Fuzz.privatekey_group_to_ETH_address_bytes.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]  # pvk,m,ret
# --------------------------------------------------------------------------------------
Fuzz.init_P2_Group.argtypes = [ctypes.c_char_p]  # upub
# --------------------------------------------------------------------------------------
Fuzz.free_memory.argtypes = [ctypes.c_void_p]  # pointer
# --------------------------------------------------------------------------------------
Fuzz.bloom_check_add.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_ulonglong, ctypes.c_ubyte,
                                 ctypes.c_char_p]  # buff, len, 0_1, _bits, _hashes, _bf
Fuzz.bloom_check_add.restype = ctypes.c_int
# --------------------------------------------------------------------------------------
Fuzz.bloom_batch_add.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_ulonglong,
                                 ctypes.c_ubyte, ctypes.c_char_p]  # chunk, buff, len, 0_1, _bits, _hashes, _bf
# --------------------------------------------------------------------------------------
Fuzz.bloom_check_add_mcpu.argtypes = [ctypes.c_void_p, ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_int, ctypes.c_int,
                                      ctypes.c_int, ctypes.c_ulonglong, ctypes.c_ubyte,
                                      ctypes.c_char_p]  # buff, num_items, found_array, len, mcpu, 0_1, _bits, 
# _hashes, _bf
# --------------------------------------------------------------------------------------
Fuzz.test_bit_set_bit.argtypes = [ctypes.c_char_p, ctypes.c_ulonglong, ctypes.c_int]  # _bf, _bits, 0_1
# --------------------------------------------------------------------------------------
Fuzz.create_bsgs_bloom_mcpu.argtypes = [ctypes.c_int, ctypes.c_ulonglong, ctypes.c_ulonglong, ctypes.c_ubyte,
                                        ctypes.c_char_p]  # mcpu, num_items, _bits, _hashes, _bf
# --------------------------------------------------------------------------------------
Fuzz.bsgs_2nd_check_prepare.argtypes = [ctypes.c_ulonglong]  # bP_elem
# --------------------------------------------------------------------------------------
Fuzz.bsgs_2nd_check.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_ulonglong,
                                ctypes.c_char_p]  # upub, z1, bP_elem, ret
# --------------------------------------------------------------------------------------
Fuzz.bsgs_2nd_check.restype = ctypes.c_bool  # True or False
# --------------------------------------------------------------------------------------
Fuzz.Load_data_to_memory.argtypes = [ctypes.c_char_p, ctypes.c_bool]  # sorted_bin_file_h160, verbose
# --------------------------------------------------------------------------------------
Fuzz.check_collision.argtypes = [ctypes.c_char_p]  # h160
# --------------------------------------------------------------------------------------
Fuzz.check_collision.restype = ctypes.c_bool  # True or False
# --------------------------------------------------------------------------------------
Fuzz.init_secp256_lib()
# --------------------------------------------------------------------------------------
