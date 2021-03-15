import secrets
Pcurve = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 -1 
N='0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141' 
Acurve = 0; Bcurve = 7 
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
GPoint = (Gx,Gy) 
def privKeyGeneration():

    privKey= secrets.randbelow(int(N,16))
    return privKey
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
    if ScalarHex == 0 or ScalarHex >= int(N,16) :
       return "0"
    ScalarBin = str(bin(ScalarHex))[2:]
    
    Q=GenPoint
   
    for i in range (1, len(ScalarBin)): 
        Q=ECdouble(Q)
        if ScalarBin[i] == "1":
            Q=ECadd(Q,GenPoint);
           
    return (Q[0],Q[1])