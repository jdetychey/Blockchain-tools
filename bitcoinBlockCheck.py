## we need dateutil and tim to convert to UNIX timestamp
import dateutil
from dateutil.parser import parse 
import time
## hashlibe is for the hashing obv
import hashlib

##str2le convert the hex to little endian 
def str2le(s):
 return "".join(reversed([s[i:i+2] for i in range(0, len(s), 2)]))
 
## the rest of the code is inspired from https://en.bitcoin.it/wiki/Block_hashing_algorithm
## the following numbers are for block 435411 see:
## https://blockchain.info/block/0000000000000000007da0f9cf1286306bb974fd0028fd163dcfd4c8813e98d8
## Blockheader on website:
version_ = "536870912"
hashPrevBlock_ = "00000000000000000152cd3a2ca9a0e9495d74570a84251e2f653e19c333362a"
hashMerkleRoot_ = "21cca5a86df0d269f93fe4c861776f73d0b83e5083803fc3a49f8ad01660e767"
blocktime_ = "2016-10-22 12:00:42"
bits_ = "402931908"
nonce_ = "3038619565"
## Blockheader:
version = str2le(hex(int(version_))[2:])
hashPrevBlock = str2le(hashPrevBlock_)#.decode("hex")
hashMerkleRoot = str2le(hashMerkleRoot_)#.decode("hex")
##converting timestamp "2016-10-22 12:00:42" unix is a pain
##BEWARE blockchain.info is in UTC but other explorer may not (ex blockexplorer.com is +2 hours)
blocktime_ = '2016-10-22 12:00:42'
unix = int(time.mktime(dateutil.parser.parse(blocktime_, parserinfo=None) .timetuple()))
timeUnix = str2le(hex(unix)[2:])

bits = str2le(hex(int(bits_))[2:])
nonce = str2le(hex(int(nonce_))[2:])

##Now we have the proper header in hex:
header_hex = version + hashPrevBlock + hashMerkleRoot + timeUnix + bits + nonce

##let's hash!:
header_bin = header_hex.decode('hex')
hash = hashlib.sha256(hashlib.sha256(header_bin).digest()).digest()
hash_hex = hash.encode('hex_codec')
hash_final = hash[::-1].encode('hex_codec')
##And this is where the magic happens:
print hash_final
