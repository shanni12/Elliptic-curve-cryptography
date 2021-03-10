import tkinter as tk
import ellipticcurve
import signatureGV
import hashlib
import json
window = tk.Tk()

label=tk.Label(text="Elliptic curve cryptography",width=100,height=10)
label.pack()
label1=tk.Label(text="Enter private key")
label1.pack()
text=tk.Entry(fg="blue")
text.pack()
def generatePrivateKey(self):
    privKey=ellipticcurve.privKeyGeneration()
    text.delete(0,tk.END)
    text.insert(0,str(privKey))

button= tk.Button(text="Click to generate random private key")
button.bind("<Button-1>",generatePrivateKey)

button.pack()
label2=tk.Label(text="Public Key")
label2.pack()
text2=tk.Entry()
text2.pack()

def generatePublicKey(self):
       
        global pub
        privKey = int(text.get())
        pub = ellipticcurve.EccMultiply(ellipticcurve.GPoint,privKey)
        text2.delete(0,tk.END)
        text2.insert(0,str(pub))
        text2.config(state="readonly")
button1= tk.Button(text="Click to get public key")
button1.bind("<Button-1>",generatePublicKey)
button1.pack()
label5=tk.Label(text="Enter the msg")
label5.pack()
text1=tk.Entry()
text1.pack()
label3=tk.Label(text="Generate Signature")
label3.pack()
text3=tk.Entry()
text3.pack()
def crypto_hash(*args):
   stringified_args=sorted(map(lambda data:json.dumps(data),args))
   
   joined_data=''.join(stringified_args)

   return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()
def generateSignature(self):
        
        data = str(text1.get())
        hash_datahex = crypto_hash(data)
        hashval = int("0x"+hash_datahex, 16)
        sig = signatureGV.signature_generation(int(text.get()),hashval)
        text3.delete(0,tk.END)
        text3.insert(0,(str(sig)))
        
button2=tk.Button(text="Click to get Signature")
button2.bind("<Button-1>",generateSignature)
button2.pack()

label4=tk.Label(text="Verify signature")
label4.pack()
text4=tk.Entry()
text4.pack()


def verifySignature(self):
        msg_rec = str(text1.get())
        hash_datahex = crypto_hash(msg_rec)
        hashval = int("0x"+hash_datahex, 16)
        sig=[1,2]
        sig[0]=int(str(text3.get()).split(",")[0][1:])
        sig[1]=int(str(text3.get()).split(",")[1][:-1])
        ver = signatureGV.signature_verification(pub,sig[0],sig[1],hashval)
        if ver == True:
            text4.delete(0,tk.END)
            text4.insert(0,"Signature verified")
        else :
             text4.delete(0,tk.END)
             text4.insert(0,"Not verified")
        
button3= tk.Button(text="click to verify signature")
button3.bind("<Button-1>",verifySignature)
button3.pack()

window.mainloop()