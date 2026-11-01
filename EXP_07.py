import hashlib, hmac
UID="2024300119"
print("EXPERIMENT 07: HASH FUNCTIONS AND HMAC"); print("UID:",UID)
original=input("\nEnter Original Message: "); modified=input("Enter Modified Message: ")
key=hashlib.sha256((UID+"CNS-HMAC-KEY").encode()).digest()
print("\nSecret Key Generated Successfully!")
algorithms={"MD5":hashlib.md5,"SHA-1":hashlib.sha1,"SHA-256":hashlib.sha256,"SHA-512":hashlib.sha512}
print("\n========== HASH VALUES ==========")
for name,alg in algorithms.items():
    print("\n",name,"\nOriginal Hash:",alg(original.encode()).hexdigest(),"\nModified Hash:",alg(modified.encode()).hexdigest())
print("\n========== HMAC VALUES ==========")
for name,alg in algorithms.items():
    print("\nHMAC-"+name,"\nOriginal HMAC:",hmac.new(key,original.encode(),alg).hexdigest(),"\nModified HMAC:",hmac.new(key,modified.encode(),alg).hexdigest())
print("\n========== TAMPERING DETECTION ==========")
om=hmac.new(key,original.encode(),hashlib.sha256).hexdigest(); mm=hmac.new(key,modified.encode(),hashlib.sha256).hexdigest()
print("No Tampering Detected" if hmac.compare_digest(om,mm) else "Tampering Detected!")
print("\n========== MAC VERIFICATION =========="); received_mac=om
for message in [original,modified]:
    calc=hmac.new(key,message.encode(),hashlib.sha256).hexdigest()
    print(message,":","PASS" if hmac.compare_digest(received_mac,calc) else "FAIL")
print("\n========== KEY SENSITIVITY ==========")
message="NetworkSecurity"; key2=hashlib.sha256((UID+"CNS-HMAC-KEY-2").encode()).digest()
for name,alg in algorithms.items():
    m1=hmac.new(key,message.encode(),alg).hexdigest(); m2=hmac.new(key2,message.encode(),alg).hexdigest()
    print("\nHMAC-"+name,"\nKey 1:",m1,"\nKey 2:",m2,"\nSame:",hmac.compare_digest(m1,m2))
