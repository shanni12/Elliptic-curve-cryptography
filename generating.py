import secrets
from nummaster.basic import sqrtmod
Pcurve = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 -1 
N='0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141' 
Acurve = 0; Bcurve = 7 
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
GPoint = (Gx,Gy) 
privKey= secrets.randbelow(int(N,16))
RandNum =secrets.randbelow(int(N,16)) #replace with a truly random number
HashOfThingToSign=86032112319101611046176971828093669637772856272773459297323797145286374828050

print(type(privKey))

def modinv(a,n=Pcurve): 
    lm, hm = 1,0
    low, high = a%n,n
    while low > 1:
        ratio = high//low
        nm, new = hm-lm*ratio, high-low*ratio
        lm, low, hm, high = nm, new, lm, low
    return lm%n

def ECadd(a,b): 
    LamAdd = ((b[1]-a[1]) * modinv(b[0]-a[0],Pcurve)) % Pcurve
    x = (LamAdd*LamAdd-a[0]-b[0]) % Pcurve
    y = (LamAdd*(a[0]-x)-a[1]) % Pcurve
    return (x,y)

def ECdouble(a): 
    Lam = ((3*a[0]*a[0]+Acurve) * modinv((2*a[1]),Pcurve)) % Pcurve
    x = (Lam*Lam-2*a[0]) % Pcurve
    y = (Lam*(a[0]-x)-a[1]) % Pcurve
    return (x,y)

def EccMultiply(GenPoint,ScalarHex): 
    if ScalarHex == 0 or ScalarHex >= int(N,16): raise Exception("Invalid Scalar/Private Key")
    ScalarBin = str(bin(ScalarHex))[2:]
    
    Q=GenPoint
   
    for i in range (1, len(ScalarBin)): 
        Q=ECdouble(Q)
        if ScalarBin[i] == "1":
            Q=ECadd(Q,GenPoint);
           
    return (Q)


def compress_point(point):
    return (point[0], point[1] % 2)

def uncompress_point(compressed_point, p, a, b):
    x, is_odd = compressed_point
    y = sqrtmod(pow(x, 3, p) + a * x + b, p)
    if bool(is_odd) == bool(y & 1):
        return (x, y)
    return (x, p - y)



PublicKey = EccMultiply(GPoint,privKey)
print("the private key:")
print(privKey)
print("Public Key")
print(PublicKey)
print("Compressed form of public key:")
compressed_point=compress_point(PublicKey)
print(compressed_point)

if PublicKey[1] % 2 == 1: 
    print ("03"+str(hex(PublicKey[0])[2:]).zfill(64))
else: 
    print("02"+str(hex(int(PublicKey[0]))[2:]).zfill(64))
print("Signature Generation")

xRandSignPoint, yRandSignPoint = EccMultiply(GPoint,RandNum)
r = xRandSignPoint % int(N,16)
s = ((HashOfThingToSign + r*privKey)*(modinv(RandNum,int(N,16)))) % int(N,16)
print("Signature Verification")
w = modinv(s,int(N,16))
xu1, yu1 = EccMultiply(GPoint,(HashOfThingToSign * w)%int(N,16))
xu2, yu2 = EccMultiply(PublicKey,(r*w)%int(N,16))
x,y = ECadd((xu1,yu1),(xu2,yu2))
print(r==x)