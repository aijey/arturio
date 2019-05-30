import math
def sqr(a):
    return a*a
cnt = {}
seredn = 0
def calc(k):
    global cnt
    res = 0
    for i in cnt.keys():
        res+=cnt[i]*(i**k)
        print(res)
    res/=40
    return res
def calc2(k):
    global cnt,seredn
    res = 0
    for i in cnt.keys():
        res+=cnt[i]*((i-seredn)**k)
    res/=40
    return res
sum = 0
while (True):
    st = input()
    if (st == "END"):
        break;
    st = st.split(' ')
    a = float(st[0])
    b = float(st[1])
    cnt[a] = b
    seredn += a*b
    sum += b
seredn/=sum
print(seredn)
res = 0
for i in cnt.keys():
    res+=cnt[i]*sqr(i-seredn)
res/=sum
print(res)
print(math.sqrt(res))
res*=40
res/=39
print(res)
print(math.sqrt(res))
for i in range(1,5):
    print("K" + str(i) + ": " + str(seredn**i))
    print(calc(i))
for i in range(1,5):
    print("k" + str(i) + ": " + str(round(calc2(i),10)))

# -2 1
# -1 1
# 0 4
# 2 4
# 3 4
# 4 3
# 5 3
# 6 1
# 7 2
# 8 2
# 9 1
# 10 2
# 11 2
# 12 2
# 13 1
# 15 1
# 17 1
# 19 2
# 21 1
# 22 2

# -2 1
# -1 1
# 0 3
# 1 1
# 1.5 1
# 2 4
# 3 4
# 4 3
# 5 1
# 6 1
# 7 2
# 8 2
# 9 1
# 10 2
# 11 2
# 12 3
# 13 1
# 15 1
# 17 2
# 19 1
# 21 1
# 22 2
# END

# prkhvtl
# -2 2
# -1 2
# 0 3
# 1 2
# 1.5 1
# 2 3
# 3 3
# 4 1
# 5 3
# 7 2
# 8 2
# 10 2
# 11 2
# 12 3
# 13 2
# 17 3
# 19 2
# 21 1
# 22 1
