import math, random, time
UID="2024300119"
def get_uid_bases(uid):
    d=[int(x) for x in uid]
    v=[int(uid[-2:]),sum(d),int(uid[:4])+int(uid[-4:]),sum(d[::2]),sum(d[1::2])]
    return [(x%97)+2 for x in v]
def get_valid_bases(n,bases):
    valid=[]
    for b in bases:
        if b>=n-1 or math.gcd(b,n)!=1:
            if n<=4: valid.append(2)
            else:
                b=random.randint(2,n-2)
                while math.gcd(b,n)!=1: b=random.randint(2,n-2)
        else: valid.append(b); continue
        if n>4: valid.append(b)
    return valid
def fermat_test(n,b):
    if n<=1:return "Composite"
    if n in (2,3):return "Prime"
    if n%2==0:return "Composite"
    return "Composite" if any(pow(a,n-1,n)!=1 for a in b) else "Prime"
def euler_test(n,b):
    if n<=1:return "Composite"
    if n in (2,3):return "Prime"
    if n%2==0:return "Composite"
    return "Composite" if any(pow(a,(n-1)//2,n) not in (1,n-1) for a in b) else "Prime"
def miller_rabin_test(n,b):
    if n<=1:return "Composite"
    if n in (2,3):return "Prime"
    if n%2==0:return "Composite"
    r,d=0,n-1
    while d%2==0:r+=1; d//=2
    for a in b:
        x=pow(a,d,n)
        if x in (1,n-1):continue
        for _ in range(r-1):
            x=pow(x,2,n)
            if x==n-1:break
        else:return "Composite"
    return "Prime"
print("UID:",UID)
derived=get_uid_bases(UID); print("Derived Bases:",derived)
n=int(input("\nEnter a number to check: "))
bases=get_valid_bases(n,derived); print("Valid Bases:",bases)
for name,fn in [("Fermat",fermat_test),("Euler",euler_test),("Miller-Rabin",miller_rabin_test)]:
    t=time.perf_counter(); result=fn(n,bases); elapsed=(time.perf_counter()-t)*1000
    print("\nAlgorithm:",name,"\nResult:",result,"\nExecution Time:",round(elapsed,6),"ms")
