# 12/16/2018
# Qing Yu Cornell ECE
# This is the program using HeteroCL language to implement Radix Sort Algorithm
# Counting sort algorithm is used inside the radix sort algorithm
##################################################################################
# Import Library
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

# counting sort function
def countSort(A, B): 
    # The output character array that will have sorted arr 
    output_A = hcl.compute((arrayLength,), lambda x: 0)
    output_B = hcl.compute((arrayLength,), lambda x: 0)
    # Create a count array to store count of inidividul 
    # characters and initialize count array as 0 
    count = hcl.compute((10,), lambda x: 0)
    # Store count of each character 
    with hcl.for_(0, arrayLength, name = 'a')as a: 
        index = hcl.local(B[a])
        count[index] += 1
  
    # Change count[i] so that count[i] now contains actual 
    # position of this character in output array 
    with hcl.for_(1,10,name='i')as i: 
        count[i] += count[i-1] 
  
    # Build the output character array 
    with hcl.for_(arrayLength-1, -1, -1, name='j')as j: 
        output_B[count[B[j]]-1] = B[j]
        output_A[count[B[j]]-1] = A[j]
        count[B[j]] -= 1
  
    # Copy the output array to arr, so that arr now 
    # contains sorted characters 
    with hcl.for_(0, arrayLength, name ='k')as k: 
        A[k] = hcl.local(output_A[k])
        

# this function is used to organize the digits of the array A 
def radix_sort(A, B):
   currDigit = hcl.local(0)
   with hcl.for_(1, numSize+1, name='i')as i:
     #construct the for loop for calculate the pow()
     pow_ = hcl.local(1)
     with hcl.for_(0, i-1):
       pow_[0] *= 10
     first_p = pow_[0] * 10
     sec_p = pow_[0]
     #factor out the digits
     with hcl.for_(0, arrayLength, name='j') as j:
       # modulate the number for first digit
       current_digit = hcl.local(A[j]% first_p)
       with hcl.if_(i>1):
         # factor out the number for upper digits
         current_digit = current_digit/sec_p
       #construct B array for containing all digits
       B[j] = current_digit
     # call the counting sort function to sort the array A by B
     countSort(A, B)
     
with hcl.Stage() as Out:
    radix_sort(A, B)

s = hcl.create_schedule([A])

#print hcl.lower(s)

f = hcl.build(s,target="llvm")

#hcl_A = hcl.asarray([24,8,32,65,88,98,546,2,7,352]) 
hcl_A = hcl.asarray(np.random.randint(500, size=(arrayLength,)))
print hcl_A
f(hcl_A)
print hcl_A     
