import secrets
import ellipticcurve

N=ellipticcurve.N
GPoint=ellipticcurve.GPoint

def signature_generation(privKey,HashOfThingToSign):
    print("Signature Generation")
    RandNum= secrets.randbelow(int(N,16))
    xRandSignPoint, yRandSignPoint = ellipticcurve.EccMultiply(GPoint,RandNum)
    r = xRandSignPoint % int(N,16)
    s = ((HashOfThingToSign + r*privKey)*(ellipticcurve.modinv(RandNum,int(N,16)))) % int(N,16)
    return (r,s)
def signature_verification(PublicKey,r,s,HashOfThingToSign):
    print("Signature Verification")
    w = ellipticcurve.modinv(s,int(N,16))
    xu1, yu1 = ellipticcurve.EccMultiply(GPoint,(HashOfThingToSign * w)%int(N,16))
    xu2, yu2 = ellipticcurve.EccMultiply(PublicKey,(r*w)%int(N,16))
    x,y = ellipticcurve.ECadd((xu1,yu1),(xu2,yu2))
    print(r==x)
    return r==x

