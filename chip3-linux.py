from bitcoinlib.encoding import bip38_decrypt
from bitcoinaddress import Wallet
from Crypto.Cipher import AES
import scrypt
import base58
import binascii
import hashlib
import bit
from bit import *
import time
import random
import multiprocessing as mp

f1 = '4bip38.txt'
bip_list = [k.split()[0] for k in open(f1,'r')]
ss = '1JxWyNrkgYvgsHu8hVQZqTXEB9RftRGP5m'

encrypted_privkey='6PnQmAyBky9ZXJyZBv9QSGRUXkKh9HfnVsZWPn4YtcwoKy5vufUgfA3Ld7'
     
def main(counter):
 while True:
    with counter.get_lock():
        counter.value += 1
    passphrase = random.choice(bip_list)+'-'+random.choice(bip_list)+'-'+random.choice(bip_list)+'-'+random.choice(bip_list)+'-'+random.choice(bip_list)
    d = base58.b58decode(encrypted_privkey)
    d = d[2:]
    flagbyte = d[0:1]
    d = d[1:]
    if flagbyte == '\xc0':
        compressed = False
    if flagbyte == '\xe0':
        compressed = True
    addresshash = d[0:4]
    d = d[4:-4]
    key = scrypt.hash(passphrase,addresshash, 16384, 8, 8)
    derivedhalf1 = key[0:32]
    derivedhalf2 = key[32:64]
    encryptedhalf1 = d[0:16]
    encryptedhalf2 = d[16:32]
    aes = AES.new(derivedhalf2,1)
    decryptedhalf2 = aes.decrypt(encryptedhalf2)
    decryptedhalf1 = aes.decrypt(encryptedhalf1)
    priv = decryptedhalf1 + decryptedhalf2
    priv = binascii.unhexlify('%064x' % (int(binascii.hexlify(priv), 16) ^ int(binascii.hexlify(derivedhalf1), 16)))
    F=priv.hex()
    C1=Key.from_hex(F)
    caddr1 = C1.address
    #check = urllib.request.urlopen("https://blockchain.info/q/getreceivedbyaddress/" + caddr1).read()
    # print(caddr1)
    #print(f"\r[+] Поиск:{passphrase}", end='', flush=True)
    #if int (check) != 0:
    #    print('HEX:' , F)
    #    print('Address compressed:' , caddr1,'Received :' + str(check.decode('UTF8')))    
    if str(caddr1) == ss:
        print(passphrase)
        print(priv.hex())
        s1 = priv.hex()
        s2 = passphrase
        f=open(u"Found.txt","a") 
        f.write(s1+"  "+s2)
        f.write("\n")
        f.close()
        break
        
    if (counter.value)%10 == 0:
           time1=time.time() - start
           kps = int(counter.value/time1)
           print('{+} [Running...] ',counter.value,' in ',round(time1),' seconds',' ', kps, 'keys p/s   ', end='\r') 
                           
if __name__ == '__main__':
    counter = mp.Value('L')
    thread = int(10)
    start = time.time()
    for cpu in range(thread):
        mp.Process(target = main, args=(counter,)).start()