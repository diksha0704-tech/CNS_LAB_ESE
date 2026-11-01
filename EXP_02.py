import numpy as np, random, math
UID="2024300119"; A="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
print("UID:",UID)
caesar_key=(sum(map(int,UID))%25)+1
random.seed(int(UID)); ml=list(A); random.shuffle(ml); mono_key=''.join(ml)
groups=[UID[i:i+2] for i in range(0,10,2)]
vigenere_key=''.join(A[int(g)%26] for g in groups)
playfair_keyword=''.join(dict.fromkeys(vigenere_key))
print("CAESAR KEY:",caesar_key,"\nMONOALPHABETIC:",mono_key,"\nVIGENERE KEY:",vigenere_key,"\nPLAYFAIR KEYWORD:",playfair_keyword)
def transform(text,key,mode="caesar",decrypt=False):
    out=""; ki=0
    for ch in str(text):
        if not ch.isalpha():out+=ch; continue
        p=A.index(ch.upper())
        if mode=="caesar":out+=A[(p+(-key if decrypt else key))%26]
        elif mode=="mono":out+=A[key.index(ch.upper())] if decrypt else key[p]
        elif mode=="vigenere":
            k=A.index(key[ki%len(key)]); out+=A[(p+(-k if decrypt else k))%26]; ki+=1
    return out
def create_playfair_matrix(keyword):
    letters=list(dict.fromkeys((keyword+A.replace("J","I")).upper().replace("J","I")))
    letters=[c for c in letters if c.isalpha()]
    return [letters[i:i+5] for i in range(0,25,5)]
def pos(m,ch):
    ch=ch.upper().replace("J","I")
    for r in range(5):
        for c in range(5):
            if m[r][c]==ch:return r,c
    raise ValueError("Character not found")
def prep(t):
    t=''.join(c for c in str(t).upper() if c.isalpha()).replace("J","I"); out=""; i=0
    while i<len(t):
        a=t[i]
        if i+1<len(t):
            b=t[i+1]
            if a==b:out+=a+("Q" if a=="X" else "X"); i+=1
            else:out+=a+b; i+=2
        else:out+=a+"X"; i+=1
    return out
def playfair(t,m,dec=False):
    if dec:
        t=''.join(c for c in str(t).upper() if c.isalpha()).replace("J","I")
        if len(t)%2:raise ValueError("Ciphertext must have even length")
    else:t=prep(t)
    out=""
    for i in range(0,len(t),2):
        a,b=t[i],t[i+1]; r1,c1=pos(m,a); r2,c2=pos(m,b)
        if r1==r2:
            s=-1 if dec else 1; out+=m[r1][(c1+s)%5]+m[r2][(c2+s)%5]
        elif c1==c2:
            s=-1 if dec else 1; out+=m[(r1+s)%5][c1]+m[(r2+s)%5][c2]
        else:out+=m[r1][c2]+m[r2][c1]
    return out
def hill_key(uid):
    k=np.array([int(uid[i:i+2]) for i in range(0,8,2)]).reshape(2,2)%26
    while math.gcd(int(round(np.linalg.det(k)))%26,26)!=1:k[0][0]=(k[0][0]+1)%26
    return k
def inv(a,m=26):
    for x in range(1,m):
        if a*x%m==1:return x
def hill_inverse(k):
    a,b=k[0]; c,d=k[1]; det=int((a*d-b*c)%26)
    if math.gcd(det,26)!=1:raise ValueError("Hill matrix is not invertible")
    return (inv(det)*np.array([[d,-b],[-c,a]]))%26
def hill(t,k,dec=False):
    t=''.join(c.upper() for c in str(t) if c.isalpha())
    if dec:
        if len(t)%2:raise ValueError("Ciphertext must have even length")
        k=hill_inverse(k)
    elif len(t)%2:t+="X"
    out=""
    for i in range(0,len(t),2):
        v=np.array([A.index(t[i]),A.index(t[i+1])]); o=np.dot(k,v)%26
        out+=''.join(A[int(x)] for x in o)
    return out
matrix=create_playfair_matrix(playfair_keyword); hk=hill_key(UID)
print("\nPLAYFAIR MATRIX")
for row in matrix:print(' '.join(row))
print("\nHILL KEY MATRIX:",hk,"\nINVERSE HILL KEY MATRIX:",hill_inverse(hk))
print("\n1. Caesar\n2. Monoalphabetic\n3. Vigenere\n4. Playfair\n5. Hill")
choice=int(input("Enter your choice: ")); op=int(input("1. Encryption\n2. Decryption\nEnter operation: "))
txt=input("Enter your text: "); dec=(op!=1)
if choice==1: result=transform(txt,caesar_key,"caesar",dec)
elif choice==2: result=transform(txt,mono_key,"mono",dec)
elif choice==3: result=transform(txt,vigenere_key,"vigenere",dec)
elif choice==4: result=playfair(txt,matrix,dec)
elif choice==5: result=hill(txt,hk,dec)
else: result="Invalid cipher choice!"
print("Ciphertext:" if op==1 else "Plaintext:",result)
