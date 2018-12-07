import heterocl as hcl
import numpy as np
#import tvm
import time
hcl.init()

n=65535
start = time.time()

#insertion sort function 
def sort(A):
    with hcl.for_(1, n, name="i") as i:
      with hcl.for_(0, i, name="j")as j:
        with hcl.if_(A[j]>A[i]):
          temp = hcl.local(A[j])
          A[j] = A[i]
          A[i] = temp

A = hcl.placeholder((n,))

#call the function
with hcl.Stage() as Out:
  sort(A)

s = hcl.create_schedule([A])
x_outer = hcl.local(0)
x_inner = hcl.local(0)
x_outer, x_inner = s[Out].split(Out.i, factor=250)
x_outer2, x_inner2 = s[Out].split(x_outer, 250)
#s[Out].split(x_outer2, 5)
#print (x_outer, x_inner)

#print hcl.lower(s)

f = hcl.build(s,target="llvm")


#hcl_A = hcl.asarray([3,1,5,6,0,4])
hcl_A = hcl.asarray(np.random.randint(2000, size=(n,)))
#print hcl_A
f(hcl_A)
print hcl_A
print time.time()-start
