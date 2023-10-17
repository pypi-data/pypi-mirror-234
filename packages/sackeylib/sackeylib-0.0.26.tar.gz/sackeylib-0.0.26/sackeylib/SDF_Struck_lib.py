from ctypes import *


SGD_SM1_ECB = 0x00000101
SGD_SM1_CBC = 0x00000102
SGD_SM1_CFB = 0x00000104
SGD_SM1_OFB = 0x00000108
SGD_SM1_MAC = 0x00000110
SGD_SM1_CTR = 0x00000120
SGD_SM1_XTS = 0x00000140

SGD_SM4_ECB = 0x00000401
SGD_SM4_CBC = 0x00000402
SGD_SM4_CFB = 0x00000404
SGD_SM4_OFB = 0x00000408
SGD_SM4_MAC = 0x00000410

SGD_DES_ECB = 0x00001001
SGD_DES_CBC = 0x00001002
SGD_DES_CFB = 0x00001004
SGD_DES_OFB = 0x00001008
SGD_DES_MAC = 0x00001010
SGD_DES_CTR = 0x00001020

SGD_3DES_ECB = 0x00002001
SGD_3DES_CBC = 0x00002002
SGD_3DES_CFB = 0x00002004
SGD_3DES_OFB = 0x00002008
SGD_3DES_MAC = 0x00002010
SGD_3DES_CTR = 0x00002020

SGD_AES128_ECB = 0x00004001
SGD_AES128_CBC = 0x00004002
SGD_AES128_CFB = 0x00004004
SGD_AES128_OFB = 0x00004008
SGD_AES128_MAC = 0x00004010

SGD_AES256_ECB = 0x00008001
SGD_AES256_CBC = 0x00008002
SGD_AES256_CFB = 0x00008004
SGD_AES256_OFB = 0x00008008
SGD_AES256_MAC = 0x00008010

SGD_RSA = 0x00010000
SGD_RSA_SIGN = 0x00010100
SGD_RSA_ENC = 0x00010200
SGD_SM2 = 0x00020100
SGD_ECC_SIGN = 0x00020200
SGD_ECC_ENC = 0x00020800
SGD_SM2_1 = 0x00020200
SGD_SM2_2 = 0x00020400
SGD_SM2_3 = 0x00020800

SGD_ECC = 0x00080100

SGD_SM3 = 0x00000001
SGD_SHA1 = 0x00000002
SGD_SHA256 = 0x00000004
SGD_SHA512 = 0x00000008
SGD_SHA224 = 0x00000010
SGD_SHA384 = 0x00000020
SGD_MD5 = 0x00000040

SGD_SM3_RSA = 0x00010001
SGD_SHA1_RSA = 0x00010002
SGD_SHA256_RSA = 0x00010004
SGD_SM3_SM2 = 0x00020201

RSAref_MAX_BITS = 2048
RSAref_MAX_LEN = int((RSAref_MAX_BITS + 7) / 8)
RSAref_MAX_PBITS = int((RSAref_MAX_BITS + 1) / 2)
RSAref_MAX_PLEN = int((RSAref_MAX_PBITS + 7)/ 8)

#ifdef SGD_MAX_ECC_BITS_256
ECCref_MAX_BITS = 256
#else
ECCref_MAX_BITS = 512
#endif

ECCref_MAX_LEN = int((ECCref_MAX_BITS+7) / 8)


SGD_MAX_COUNT = 64
SGD_MAX_NAME_SIZE = 256


class SDF_ERR_REASON(Structure):
    _fields_ = [("err", c_int),
                ("reason", c_ulong)]

class DEVICEINFO(Structure):
    _fields_ = [	
        ("IssuerName", c_char*40),
		("DeviceName", c_char*16),
		("DeviceSerial", c_char*16),
		("DeviceVersion", c_uint),
		("StandardVersion", c_uint),
		("AsymAlgAbility", c_uint * 2),
		("SymAlgAbility", c_uint),
		("HashAlgAbility", c_uint),
		("BufferSize", c_uint)      # 支持的最大文件存储空间(单位字节)
        ]


class TassData(Structure):
    _fields_ = [("data", c_ubyte * 1024),
                ("dataLen", c_int)]



class RSArefPublicKey(Structure):
    _fields_ = [
		("bits", c_int),
        # 模长	
		("m", c_char * RSAref_MAX_LEN),
        # 模 N
		("e", c_char * RSAref_MAX_LEN)
        # 指数
	]

class RSArefPrivateKey(Structure):
    _fields_ = [
		("bits", c_int),
        # 模长
		("m", c_char * RSAref_MAX_LEN),
        # 模 N
		("e", c_char * RSAref_MAX_LEN),
        # 指数
		("d", c_char * RSAref_MAX_LEN),
		("prime", c_char * 2 * RSAref_MAX_PLEN),
        # 素数p和q
		("pexp", c_char * 2 * RSAref_MAX_PLEN),
        # Dp和Dq
		("coef", c_char * RSAref_MAX_PLEN)
        # 系数i
	]

class ECCrefPublicKey(Structure):
    _fields_ = [
		("bits", c_int),
		("x", c_char * ECCref_MAX_LEN),
		("y", c_char * ECCref_MAX_LEN)
	]

class ECCrefPrivateKey(Structure):
    _fields_ = [
		( "bits", c_int),
		("K", c_char * ECCref_MAX_LEN)
	]

class ECCCipher(Structure):
    _fields_ = [
		("x", c_char * ECCref_MAX_LEN),
		("y", c_char * ECCref_MAX_LEN),
		("M", c_char * 32),
		("L", c_int),
		("C", c_char * ECCref_MAX_LEN)
        # TODO
	]

class ECCSignature(Structure):
    _fields_ = [
		("r", c_char * ECCref_MAX_LEN),
		("s", c_char * ECCref_MAX_LEN)
	]

class SDF_ENVELOPEDKEYB(Structure):
    _fields_ = [
		("Version", c_ulong),
		("ulSymmAlgID", c_ulong),
		("ECCCipehrBlob", ECCCipher),
		("PubKey", ECCrefPublicKey),
		("cbEncryptedPrivKey", c_char * 64)
	]







if __name__ == '__main__':
    from sackeylib.sackey_lib import *
    for var in locals().copy():
        print(var,locals()[var])

