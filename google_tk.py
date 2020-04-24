import ctypes
import sys

#无符号位移: https://www.jianshu.com/p/24d11ab44ae6
#这个函数可以得到32位int溢出结果，因为python的int一旦超过宽度就会自动转为long，永远不会溢出，有的结果却需要溢出的int作为参数继续参与运算
def int_overflow(val):
    maxint = 2147483647
    if not -maxint-1 <= val <= maxint:
        val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
    return val

def unsigned_right_shitf(n,i):
    # 数字小于0，则转为32位无符号uint
    if n<0:
        n = ctypes.c_uint32(n).value
    # 正常位移位数是为正数，但是为了兼容js之类的，负数就右移变成左移好了
    if i<0:
        return -int_overflow(n << abs(i))
    return int_overflow(n >> i)

def google_TL(src):
    a = src.strip()
    b = 406644
    b1 = 3293161072

    jd = "."
    Sb = "+-a^+6"
    Zb = "+-3^+b+-f"

    e = []
    for g in range(len(a)):
        m = ord(a[g])
        if 128 > m:
            e.append(m)
        else:
            if 2048 > m:
                e.append(m >> 6 | 192)
            else:
                if 55296 == (m & 64512) and g + 1 < len(a) and 56320 == (a[g+1] & 64512):
                    g += 1
                    m = 65535 + ((m & 1024) << 10) + (a[g] & 1023)
                    e.append(m >> 18 | 240)
                    e.append(m >> 12 & 63 | 128)
                else:
                    e.append(m >> 12 | 224)
                    e.append(m >> 6 & 63 | 128)
                e.append(m & 63 | 128)
    a = b
    for f in range(len(e)):
        a += int(e[f])
        a = google_RL(a, Sb)
    a = google_RL(a, Zb)
    if b1:
        a ^= b1
    else:
        a ^= 0
    if 0 > a:
        a = (a & 2147483647) + 2147483647
    a %= 1E6
    return str(int(a)) + jd + str(int(a) ^ b)

def google_RL(a,b):
    t = 'a'
    Yb = '+'
    for c in range(0, len(b)-2, 3):
        d = b[c+2]
        if d >= t:
            d = ord(d[0]) - 87
        else:
            d = int(d)
        if b[c+1] == Yb:
            d = unsigned_right_shitf(a,d)
        else:
            d = int(a) << d
        if b[c] == Yb:
            a = int(a) + d & 4294967295
        else:
            a = int(a) ^ d
    return a

if __name__ == '__main__':
    print(google_TL(str(sys.argv[1])))