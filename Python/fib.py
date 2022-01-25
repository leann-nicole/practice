'''
def fib(n):
    if (n == 1 or n == 2):
        return 1
    return fib(n-1) + fib(n-2)'''

# 1 1 2 3 5 8 13


def fib(n):
    num = 0
    numSub1 = 1
    numSub2 = 1
    count = 0
    while(count != n):
        count += 1
        if (count == 1 or count == 2):
            num = 1
        else:
            num = numSub1 + numSub2
            temp = numSub1
            numSub1 = num
            numSub2 = temp

    return num


for x in range(30):
    print(fib(x+1))
