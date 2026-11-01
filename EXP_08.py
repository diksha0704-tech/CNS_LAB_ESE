import os, hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, rsa, padding
from cryptography.exceptions import InvalidSignature
from pqcrypto.sign import ml_dsa_44, slh_dsa_sha2_128s
UID=os.environ.get("STUDENT_UID","2024300119")
assert UID.isdigit() and len(UID)==10
P256_N=int("FFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551",16)
ALGS={"ecdsa":"cryptography","rsapss":"cryptography","mldsa":ml_dsa_44,"slhdsa":slh_dsa_sha2_128s}
def ecdsa_scalar():
    h=hashlib.sha256((UID+"CNS-DSIG-ECDSA-KEY").encode()).digest()
    return int.from_bytes(h,"big")%(P256_N-1)+1
amount=1000+int(UID)%9000
DOC=(f"Transfer Rs.{amount} to Account {UID[-4:]}\n"+f"Issued by UID: {UID}\n").encode()
print(DOC.decode())
def keygen(alg):
    if alg=="ecdsa":
        sk=ec.derive_private_key(ecdsa_scalar(),ec.SECP256R1()); return {"sk":sk,"pk":sk.public_key()}
    if alg=="rsapss":
        sk=rsa.generate_private_key(public_exponent=65537,key_size=3072); return {"sk":sk,"pk":sk.public_key()}
    pk,sk=ALGS[alg].keygen(); return {"sk":sk,"pk":pk}
KEYS={a:keygen(a) for a in ALGS}
def sign(alg,data):
    k=KEYS[alg]
    if alg=="ecdsa":return k["sk"].sign(data,ec.ECDSA(hashes.SHA256()))
    if alg=="rsapss":
        pss=padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=hashes.SHA256().digest_size)
        return k["sk"].sign(data,pss,hashes.SHA256())
    return ALGS[alg].sign(k["sk"],data)
def verify(alg,data,sig):
    k=KEYS[alg]
    if alg=="ecdsa":
        try:k["pk"].verify(sig,data,ec.ECDSA(hashes.SHA256())); return True
        except InvalidSignature:return False
    if alg=="rsapss":
        pss=padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=hashes.SHA256().digest_size)
        try:k["pk"].verify(sig,data,pss,hashes.SHA256()); return True
        except InvalidSignature:return False
    try:ALGS[alg].verify(k["pk"],data,sig); return True
    except Exception:return False
SIGS={a:sign(a,DOC) for a in ALGS}
for a in ALGS:print(a,"valid:",verify(a,DOC,SIGS[a]))
def flip(data,index):
    b=bytearray(data); b[index]^=1; return bytes(b)
tampered_doc=flip(DOC,int(UID)%len(DOC))
for a in ALGS:
    print(a,"original:",verify(a,DOC,SIGS[a]),"tampered:",verify(a,tampered_doc,SIGS[a]))
