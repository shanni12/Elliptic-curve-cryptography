import secrets
from nummaster.basic import sqrtmod
Pcurve = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 -1 # The proven prime
N='0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141' # Number of points in the field
Acurve = 0; Bcurve = 7 # These two defines the elliptic curve. y^2 = x^3 + Acurve * x + Bcurve
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
GPoint = (Gx,Gy) 
privKey= secrets.randbelow(int(N,16))
# privKey=72759466100064397073952777052424474334519735946222029294952053344302920927294
print(type(privKey))
# def egcd(a, b):
#     if a == 0:
#         return (b, 0, 1)
#     else:
#         g, y, x = egcd(b % a, a)
#         return (g, x - (b // a) * y, y)

# def modinv(a, m=Pcurve):
#     g, x, y = egcd(a, m)
#     print("sha")
#     print(g)
#     if g != 1:
#         raise Exception('modular inverse does not exist')
#     else:
#         return x % m
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
   
    for i in range (1, len(ScalarBin)): # This is invented EC multiplication.
        Q=ECdouble(Q); # print "DUB", Q[0]; print
        if ScalarBin[i] == "1":
            Q=ECadd(Q,GenPoint);
            # print "ADD", Q[0]; print
    return (Q)


def compress_point(point):
    return (point[0], point[1] % 2)

def uncompress_point(compressed_point, p, a, b):
    x, is_odd = compressed_point
    y = sqrtmod(pow(x, 3, p) + a * x + b, p)
    if bool(is_odd) == bool(y & 1):
        return (x, y)
    return (x, p - y)
# print(str(bin(hex(privKey))))

PublicKey = EccMultiply(GPoint,privKey)
print("the private key:")
print(privKey)
print("Public Key")
print(PublicKey)
print("Compressed form of public key:")
compressed_point=compress_point(PublicKey)
print(compressed_point)
# print("the uncompressed public key (not address):")
# # uncompressed_public_key=uncompress_point(compressed_point,Pcurve,Acurve,Bcurve)
# print(uncompressed_public_key)
# print((GPoint*privKey)[0])
# print("the uncompressed public key (HEX):")
# print("04" + "%064x" +str(PublicKey[0])+ "%064x" +str(PublicKey[1]))

# print("the official Public Key - compressed:")
if PublicKey[1] % 2 == 1: # If the Y value for the Public Key is odd.
    print ("03"+str(hex(PublicKey[0])[2:]).zfill(64))
else: # Or else, if the Y value is even.
    print("02"+str(hex(int(PublicKey[0]))[2:]).zfill(64))