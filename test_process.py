import ctypes
import time
from multiprocessing import Process, Array, Value

values = [(s*4).encode('ascii') for s in 'abc']

def f1(a, v):
    for i, s in enumerate(values):
        a[i] = s

    v.value += 1

    print("f1 : ", a[:], v.value)

def f2(a,v):
    v.value += 1
    print("f2 : ", a[:], v.value)

def main(val, arr):

    print("Before :", arr[:], val.value)

    p = Process(target=f1, args=(arr, val))
    p2 = Process(target=f2, args=(arr, val))

    p.start()
    p2.start()

    print("After : ", arr[:], val.value)

if __name__ == '__main__':
    val = Value(ctypes.c_int, 0)
    arr = Array(ctypes.c_char_p, 3)

    while val.value < 100:
        main(val, arr)

    print("Done")