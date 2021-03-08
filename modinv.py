def modinv(a,n): 
    lm, hm = 1,0
    low, high = (a+n)%n,n
    while low > 1:
        ratio = high//low
        nm, new = hm-lm*ratio, high-low*ratio
        lm, low, hm, high = nm, new, lm, low
    return ((lm%n)+n)%n
print(modinv(17,5))
print(17%5)
print(19//5)