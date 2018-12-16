import heterocl as hcl
import numpy as np
import math
import time
hcl.init("int32")

# The length of array
arrayLength = 10
# The length of most significent bit
numSize = 3
#temperary array B for storing the current digt of number in the array
B = hcl.compute((arrayLength,), lambda x: 0)
A = hcl.placeholder((arrayLength,), dtype="int")

#def merge(left, right, A, tempArray, start, end):
#    index = hcl.local(0)
#    mid = hcl.local((start+end)/2)
#    with hcl.for_(left, mid+1, name="i") and with hcl.for_(right, end+1, name="j"):
#     with hcl.if_(A[i]<A[j]):
#          tempArray[index] = A[i]
#         index+=hcl.local(1)
#         left+=hcl.local(1)
#          i+=hcl.local(1)
#      with hcl.else_:
#          tempArray[index] = A[j]
#          index += hcl.local(1)
#          right += hcl.local(1)
#          j+=hcl.local(1)
          
#    with hcl.for_(left, mid, name="k"):
#      tempArray[index] = A[k]
#      index+=1
#      k+=1
#    with hcl.for_(right, end, name="k"):
#      tempArray[index] = A[k]
#      index+=1
#      k+=1
#    with hcl.for_(start, end+1, name="a"):
#      A[a] = tempArray[a]
    
#    return A
    
#insertion sort algorithm function 
def insertion_sort(A, B):
    with hcl.for_(1, arrayLength, name="i") as i:
      with hcl.for_(0, i, name="j")as j:
        with hcl.if_(B[j]>B[i]):
          temp0 = hcl.local(B[j])
          B[j] = B[i]
          B[i] = temp0
          temp = hcl.local(A[j])
          A[j] = A[i]
          A[i] = temp

# this function is used to organize the digits of the number 
def radix_sort(A, B):
   currDigit = hcl.local(0)
   with hcl.for_(1, numSize+1, name='i')as i:
     pow_ = hcl.local(1)
     with hcl.for_(0, i-1) as j:
       pow_[0] *= 10
     first_p = pow_[0] * 10
     sec_p = pow_[0]
     with hcl.for_(0, arrayLength, name='j') as j:
       current_digit = hcl.local(A[j]% first_p)
       with hcl.if_(i>1):
         current_digit = current_digit/sec_p
       B[j] = current_digit
     insertion_sort(A, B)
     
with hcl.Stage() as Out:
    radix_sort(A, B)

s = hcl.create_schedule([A])

#print hcl.lower(s)

f = hcl.build(s,target="llvm")

hcl_A = hcl.asarray([233,65,5,6,30,40,7,89,222,100])
#hcl_A = hcl.asarray(np.random.randint(500, size=(arrayLength,)))
print hcl_A
f(hcl_A)
print hcl_A     
     
   
  
  
