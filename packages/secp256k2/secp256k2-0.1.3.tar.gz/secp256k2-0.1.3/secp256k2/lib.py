import platform
import os
import sys
import ctypes
import math, pickle
from .constants import (
    MAX_HEX, ZERO_BYTE, BASE58_CHARS, PREFIX_0, PREFIX_80, PREFIX_9, PREFIX_8,
    PREFIX_7, PREFIX_6, PREFIX_5, PREFIX_4, PREFIX_3, PREFIX_2, PREFIX_1
)

if 'win' in platform.platform().lower():
    dirPath = os.path.dirname(os.path.realpath(__file__))
    secFile = dirPath + '/_secp256k1.dll'
    if os.path.isfile(secFile):
        dllPath = os.path.realpath(secFile)
        Fuzz = ctypes.CDLL(dllPath)
    else:
        raise ValueError("File {} not found".format(secFile))

if 'linux' in platform.platform().lower():
    dir_Path = os.path.dirname(os.path.realpath(__file__))
    secFile = dir_Path + '/_secp256k1.so'
    if os.path.isfile(secFile):
        dllPath = os.path.realpath(secFile)
        Fuzz = ctypes.CDLL(dllPath)
    else:
        raise ValueError("File {} not found".format(secFile))

COIN_BTC = 0
# =======================================================================
Fuzz.scalar_multiplication.argtypes = [ctypes.c_char_p, ctypes.c_char_p]  # pvk,ret
# ==============================================================================
Fuzz.scalar_multiplications.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]  # pvk,len,ret
# ==============================================================================
Fuzz.get_x_to_y.argtypes = [ctypes.c_char_p, ctypes.c_bool, ctypes.c_char_p]  # x,even,ret
# ==============================================================================
Fuzz.point_increment.argtypes = [ctypes.c_char_p, ctypes.c_char_p]  # upub,ret
# ==============================================================================
Fuzz.point_negation.argtypes = [ctypes.c_char_p, ctypes.c_char_p]  # upub,ret
# ==============================================================================
Fuzz.point_doubling.argtypes = [ctypes.c_char_p, ctypes.c_char_p]  # upub,ret
# ==============================================================================
Fuzz.privatekey_to_coinaddress.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_bool,
                                           ctypes.c_char_p]  # intcoin,012,comp,pvk
# ==============================================================================
Fuzz.privatekey_to_coinaddress.restype = ctypes.c_void_p
# ==============================================================================
Fuzz.privatekey_to_address.argtypes = [ctypes.c_int, ctypes.c_bool, ctypes.c_char_p]  # 012,comp,pvk
# ==============================================================================
Fuzz.privatekey_to_address.restype = ctypes.c_void_p
# ==============================================================================
Fuzz.hash_to_address.argtypes = [ctypes.c_int, ctypes.c_bool, ctypes.c_char_p]  # 012,comp,hash
# ==============================================================================
Fuzz.hash_to_address.restype = ctypes.c_void_p
# ==============================================================================
Fuzz.pubkey_to_address.argtypes = [ctypes.c_int, ctypes.c_bool, ctypes.c_char_p]  # 012,comp,upub
# ==============================================================================
Fuzz.pubkey_to_address.restype = ctypes.c_void_p
# ==============================================================================
Fuzz.privatekey_to_h160.argtypes = [ctypes.c_int, ctypes.c_bool, ctypes.c_char_p, ctypes.c_char_p]  # 012,comp,pvk,ret
# ==============================================================================
Fuzz.privatekey_loop_h160.argtypes = [ctypes.c_ulonglong, ctypes.c_int, ctypes.c_bool, ctypes.c_char_p,
                                      ctypes.c_char_p]  # num,012,comp,pvk,ret
# ==============================================================================
Fuzz.privatekey_loop_h160_sse.argtypes = [ctypes.c_ulonglong, ctypes.c_int, ctypes.c_bool, ctypes.c_char_p,
                                          ctypes.c_char_p]  # num,012,comp,pvk,ret
# ==============================================================================
Fuzz.pubkey_to_h160.argtypes = [ctypes.c_int, ctypes.c_bool, ctypes.c_char_p, ctypes.c_char_p]  # 012,comp,upub,ret
# ==============================================================================
Fuzz.pbkdf2_hmac_sha512_dll.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int]  # ret, words, len
# ==============================================================================
Fuzz.pbkdf2_hmac_sha512_list.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulonglong, ctypes.c_int,
                                         ctypes.c_ulonglong]  # ret,words,len,mnem_size,total
# ==============================================================================
Fuzz.pub_endo1.argtypes = [ctypes.c_char_p, ctypes.c_char_p]  # upub,ret
# ==============================================================================
Fuzz.pub_endo2.argtypes = [ctypes.c_char_p, ctypes.c_char_p]  # upub,ret
# ==============================================================================
Fuzz.b58_encode.argtypes = [ctypes.c_char_p]  # _h
# ==============================================================================
Fuzz.b58_encode.restype = ctypes.c_void_p
# ==============================================================================
Fuzz.b58_decode.argtypes = [ctypes.c_char_p]  # addr
# ==============================================================================
Fuzz.b58_decode.restype = ctypes.c_void_p
# ==============================================================================
Fuzz.bech32_address_decode.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p]  # coin,b32_addr,h160
# ==============================================================================
Fuzz.get_sha256.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]  # input, len, ret
# ==============================================================================
Fuzz.create_baby_table.argtypes = [ctypes.c_ulonglong, ctypes.c_ulonglong, ctypes.c_char_p]  # start,end,ret
# ==============================================================================
Fuzz.point_addition.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
Fuzz.point_subtraction.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
# ==============================================================================
Fuzz.point_loop_subtraction.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_char_p,
                                        ctypes.c_char_p]
# ==============================================================================
Fuzz.point_loop_addition.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_char_p,
                                     ctypes.c_char_p]
# ==============================================================================
Fuzz.point_vector_addition.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_char_p,
                                       ctypes.c_char_p]
# ==============================================================================
Fuzz.point_sequential_increment_P2.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_char_p]  # num,upub1,ret
# ==============================================================================
Fuzz.point_sequential_increment_P2_mcpu.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_int,
                                                    ctypes.c_char_p]  # num,upub1,mcpu,ret
# ==============================================================================
Fuzz.point_sequential_increment.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_char_p]  # num,upub1,ret
# ==============================================================================
Fuzz.point_sequential_decrement.argtypes = [ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_char_p]  # num,upub1,ret
# ==============================================================================
Fuzz.pubkeyxy_to_ETH_address.argtypes = [ctypes.c_char_p]  # upub_xy
Fuzz.pubkeyxy_to_ETH_address.restype = ctypes.c_void_p
# ==============================================================================
Fuzz.pubkeyxy_to_ETH_address_bytes.argtypes = [ctypes.c_char_p, ctypes.c_char_p]  # upub_xy, ret
# ==============================================================================
Fuzz.privatekey_to_ETH_address.argtypes = [ctypes.c_char_p]  # pvk
Fuzz.privatekey_to_ETH_address.restype = ctypes.c_void_p
# ==============================================================================
Fuzz.privatekey_to_ETH_address_bytes.argtypes = [ctypes.c_char_p, ctypes.c_char_p]  # pvk, ret
# ==============================================================================
Fuzz.privatekey_group_to_ETH_address.argtypes = [ctypes.c_char_p, ctypes.c_int]  # pvk, m
Fuzz.privatekey_group_to_ETH_address.restype = ctypes.c_void_p
# ==============================================================================
Fuzz.privatekey_group_to_ETH_address_bytes.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]  # pvk,m,ret
# ==============================================================================
Fuzz.init_P2_Group.argtypes = [ctypes.c_char_p]  # upub
# ==============================================================================
Fuzz.free_memory.argtypes = [ctypes.c_void_p]  # pointer
# ==============================================================================
Fuzz.bloom_check_add.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_ulonglong, ctypes.c_ubyte,
                                 ctypes.c_char_p]  # buff, len, 0_1, _bits, _hashes, _bf
Fuzz.bloom_check_add.restype = ctypes.c_int
# ==============================================================================
Fuzz.bloom_batch_add.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_ulonglong,
                                 ctypes.c_ubyte, ctypes.c_char_p]  # chunk, buff, len, 0_1, _bits, _hashes, _bf
# ==============================================================================
Fuzz.bloom_check_add_mcpu.argtypes = [ctypes.c_void_p, ctypes.c_ulonglong, ctypes.c_char_p, ctypes.c_int, ctypes.c_int,
                                      ctypes.c_int, ctypes.c_ulonglong, ctypes.c_ubyte,
                                      ctypes.c_char_p]  # buff, num_items, found_array, len, mcpu, 0_1, _bits,
# _hashes, _bf
# ==============================================================================
Fuzz.test_bit_set_bit.argtypes = [ctypes.c_char_p, ctypes.c_ulonglong, ctypes.c_int]  # _bf, _bits, 0_1
# ==============================================================================
Fuzz.create_bsgs_bloom_mcpu.argtypes = [ctypes.c_int, ctypes.c_ulonglong, ctypes.c_ulonglong, ctypes.c_ubyte,
                                        ctypes.c_char_p]  # mcpu, num_items, _bits, _hashes, _bf
# ==============================================================================
Fuzz.bsgs_2nd_check_prepare.argtypes = [ctypes.c_ulonglong]  # bP_elem
# ==============================================================================
Fuzz.bsgs_2nd_check.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_ulonglong,
                                ctypes.c_char_p]  # upub, z1, bP_elem, ret
# ==============================================================================
Fuzz.bsgs_2nd_check.restype = ctypes.c_bool  # True or False
# ==============================================================================
Fuzz.Load_data_to_memory.argtypes = [ctypes.c_char_p, ctypes.c_bool]  # sorted_bin_file_h160, verbose
# ==============================================================================
Fuzz.check_collision.argtypes = [ctypes.c_char_p]  # h160
# ==============================================================================
Fuzz.check_collision.restype = ctypes.c_bool  # True or False
# ==============================================================================
Fuzz.init_secp256_lib()


class Base58k1:

    def __init__(self):
        super().__init__()
        self.contactor = Contactor()

    def b58py(self, data):
        B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

        if data[0] == 0:
            return "1" + self.b58py(data[1:])

        x = sum([v * (256 ** i) for i, v in enumerate(data[::-1])])
        ret = ""
        while x > 0:
            ret = B58[x % 58] + ret
            x = x // 58

        return ret

    # ==============================================================================
    def b58_encode(self, inp_bytes):
        res = Fuzz.b58_encode(inp_bytes, len(inp_bytes))
        addr = self.contactor.fuzz256k1(res)
        Fuzz.free_memory(res)
        return addr

    # ==============================================================================
    def b58_decode(self, inp):
        res = Fuzz.b58_decode(inp.encode("utf-8"))
        addr = self.contactor.fuzz256k1(res)
        Fuzz.free_memory(res)
        return addr


class Contactor:
    def __init__(self):
        super().__init__()
        self.b58k1 = Base58k1()
    # ==============================================================================
    def version(self):
        Fuzz.version()

    def fuzz256k1(self, result):
        return ctypes.cast(result, ctypes.c_char_p).value.decode('utf8')

    # ==============================================================================
    def get_sha256(self, input_bytes):
        digest_bytes = PREFIX_0 * 32
        if type(input_bytes) == str:
            input_bytes = input_bytes.encode("utf-8")
        #    MiniKey example
        Fuzz.get_sha256(input_bytes, len(input_bytes), digest_bytes)
        return digest_bytes

    # ==============================================================================
    def Decimal_To_Addr(self, decimal: int, addr_type: int, compress: bool = True) -> str:
        """

        decimal to address (type= 0:p2pkh, 1:p2sh, 2:bech32).

        :param decimal:
        :type decimal: int.
        :param Type:
        :type Type: int.
        :param compress:
        :type compress: bool.
        :return: address.
        :rtype: str.

        ----------------------------------------------------------------------------

        >>> dec = 0x0000000000000000000000000000000000000000000000000000000000000000
        >>> compress_address = self.Decimal_To_Addr(dec, 0, True)
        >>> uncompress_address = self.Decimal_To_Addr(dec, 0, False)
        >>> # p2sh valid just compressed key
        >>> compress_p2sh = self.Decimal_To_Addr(dec, 1, True)
        >>> # bech32 valid just compressed key
        >>> compress_bech32 = self.Decimal_To_Addr(dec, 2, True)

        ----------------------------------------------------------------------------


        """
        if decimal < 0:
            pvk_int = MAX_HEX + decimal
        pass_int_value = self.fl(decimal).encode('utf8')
        res = Fuzz.privatekey_to_address(addr_type, compress, pass_int_value)
        addr = self.fuzz256k1(res)
        Fuzz.free_memory(res)
        return addr

    # ==============================================================================
    def RIPEMD160_To_Addr(self, hash160: bytes, addr_type: int, compress: bool = True) -> str:
        # type = 0 [p2pkh],  1 [p2sh],  2 [bech32]
        res = Fuzz.hash_to_address(addr_type, compress, hash160)
        addr = self.fuzz256k1(res)
        Fuzz.free_memory(res)
        return addr

    # ==============================================================================
    def Wif_To_Hex(self, wif):
        pvk = ''
        if wif[0] == '5':
            pvk = self.b58k1.b58_decode(wif)[2:-8]
        elif wif[0] in ['L', 'K']:
            pvk = self.b58k1.b58_decode(wif)[2:-10]
        else:
            raise ValueError("[Error] Incorrect WIF Key")
        return pvk

    # ==============================================================================
    def Wif_To_Decimal(self, wif):
        pvk = ''
        pvk_hex = self.Wif_To_Hex(wif)
        if pvk_hex != '': pvk = int(pvk_hex, 16)
        return pvk

    # ==============================================================================
    def Hex_To_Wif(self, pvk, compress=True):
        """ Input Privatekey can in any 1 of these [Integer] [Hex] [Bytes] form"""
        inp = ''
        suff = '01' if compress else ''
        if type(pvk) in [int, str]:
            inp = bytes.fromhex('80' + fl(pvk) + suff)
        elif type(pvk) == bytes:
            stuf = bytes.fromhex(suff)
            inp = PREFIX_80 + self.fl(pvk) + stuf
        else:
            ValueError("[Error] Input Privatekey format [Integer] [Hex] [Bytes] allowed only")
        if inp != '':
            res = self.get_sha256(inp)
            res2 = self.get_sha256(res)
            return self.b58k1.b58_encode(inp + res2[:4])
        else:
            return inp

    # ==============================================================================
    def checksum(self, inp):
        res = self.get_sha256(inp)
        res2 = self.get_sha256(res)
        return res2[:4]

    # ==============================================================================
    def fl(self, s, length=64):
        fixed = None
        if type(s) == int:
            fixed = hex(s)[2:].zfill(length)
        elif type(s) == str:
            fixed = s[2:].zfill(length) if s[:2].lower() == '0x' else s.zfill(length)
        elif type(s) == bytes:
            fixed = PREFIX_0 * 32 - len(s) + s
        else:
            ValueError("[Error] Input format [Integer] [Hex] [Bytes] allowed only. Detected : ", type(s))
        return fixed

    # ==============================================================================

    def Public_To_Addr(self, pub: bytes, addr_type: int, compress: bool = True):
        res = Fuzz.pubkey_to_address(addr_type, compress, pub)
        addr = self.fuzz256k1(res)
        Fuzz.free_memory(res)
        return addr

    # ==============================================================================

    def Decimal_To_RIPEMD160(self, dec: int, addr_type: int, compress: bool = True):
        if dec < 0: dec = MAX_HEX + dec
        pass_int_value = self.fl(dec).encode('utf8')
        res = PREFIX_0 * 20
        Fuzz.privatekey_to_h160(addr_type, compress, pass_int_value, res)
        return res

    # ==============================================================================
    def Decimal_To_RIPEMD160_DIGEST(self, dec: int, addr_type: int, compress: bool = True):
        res = self.Decimal_To_RIPEMD160(dec, addr_type, compress)
        return bytes(bytearray(res))

    # ==============================================================================

    def Pub_To_RIPEMD160(self, pub: bytes, addr_type: int, compress: bool = True):
        # type = 0 [p2pkh],  1 [p2sh],  2 [bech32]
        res = PREFIX_0 * 20
        Fuzz.pubkey_to_h160(addr_type, compress, pub, res)
        return res

    # ==============================================================================

    def Pub_To_RIPEMD160_DIGEST(self, pub: bytes, addr_type: int, compress: bool = True):
        res = self.Pub_To_RIPEMD160(pub, addr_type, compress)
        return bytes(bytearray(res))

    # ==============================================================================

    def Pub_To_Ethereum_Addr(self, pub: bytes):
        ''' 65 Upub bytes input. Output is 20 bytes ETH address lowercase with 0x as hex string'''
        xy = pub[1:]
        res = Fuzz.pubkeyxy_to_ETH_address(xy)
        addr = self.fuzz256k1(res)
        Fuzz.free_memory(res)
        return '0x' + addr

    # ==============================================================================

    def Pub_To_Ethereum_Addr_Hash(self, xy):
        res = PREFIX_0 * 20
        Fuzz.pubkeyxy_to_ETH_address_bytes(xy, res)
        return res

    # ==============================================================================

    def Pub_To_Ethereum_Addr_Digest(self, pub: bytes):
        """ 65 Upub bytes input. Output is 20 bytes ETH address lowercase without 0x"""
        xy = pub[1:]
        res = self.Pub_To_Ethereum_Addr(xy)
        return bytes(bytearray(res))

    # ==============================================================================
    def Decimal_To_ETH_Addr(self, dec: int):
        """ Privatekey Integer value passed to function. Output is 20 bytes ETH address lowercase with 0x as hex string"""
        if dec < 0: dec = MAX_HEX + dec
        pass_int_value = self.fl(dec).encode('utf8')
        res = Fuzz.privatekey_to_ETH_address(pass_int_value)
        addr = self.fuzz256k1(res)
        Fuzz.free_memory(res)
        return '0x' + addr

    # ==============================================================================

    def Decimal_To_ETH_Addr_Bytes(self, dec: int):
        res = PREFIX_0 * 20
        Fuzz.privatekey_to_ETH_address_bytes(dec, res)
        return res

    # ==============================================================================

    def Decimal_To_ETH_Addr_Digest(self, dec: int):
        """ Privatekey Integer value passed to function. Output is 20 bytes ETH address lowercase without 0x"""
        if dec < 0: dec = MAX_HEX + dec
        pass_int_value = self.fl(dec).encode('utf8')
        res = self.Decimal_To_ETH_Addr_Bytes(pass_int_value)
        return bytes(bytearray(res))

    # =============================================================================

    def Decimal_To_Batch_ETH_Addr(self, dec: int, m):
        """ Starting Privatekey Integer value passed to function as pvk_int.
        Integer m is, how many times sequential increment is done from the starting key.
        Output is bytes 20*m of ETH address lowercase without 0x as hex string"""
        if m <= 0: m = 1
        if dec < 0: dec = MAX_HEX + dec
        start_pvk = self.fl(dec).encode('utf8')
        res = Fuzz.privatekey_group_to_ETH_address(start_pvk, m)
        addrlist = self.fuzz256k1(res)
        Fuzz.free_memory(res)
        return addrlist

    # ==============================================================================

    def Load_To_Memory(self, input_bin: str, verbose: bool = False):
        """input_bin_file is sorted h160 data of 20 bytes each element.
        ETH address can also work without 0x if sorted binary format"""
        Fuzz.Load_data_to_memory(input_bin.encode("utf-8"), verbose)

    # ==============================================================================

    def Check_Collision(self, RIPEMD160):
        """ h160 is the 20 byte hash to check for collision in data, already loaded in RAM.
        Use the function Load_To_Memory before calling this check"""
        return Fuzz.check_collision(RIPEMD160)

    # ==============================================================================

    def Hex_To_Dec(self, hexed: str):
        return int(hexed, 16)

    # =============================================================================

    def Hex_To_Addr(self, hexed: str, compress: bool = True):
        dec_i = self.Hex_To_Dec(hexed)
        dec = self.fl(dec_i).encode('utf8')
        if compress:
            res = Fuzz.privatekey_to_address(0, True, dec)
        else:
            res = Fuzz.privatekey_to_address(0, False, dec)
        addr = self.fuzz256k1(res)
        Fuzz.free_memory(res)
        return addr

    # =============================================================================

    def Hex_To_Bytes(self, hexed: str) -> bytes: return bytes.fromhex(hexed)

    # =============================================================================

