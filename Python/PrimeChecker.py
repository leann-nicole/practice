
def isPrime (num):
    if num == 0 or num == 1: return False
    if num != 2:
        for i in range(2,num):
            if num % i == 0 :return False
    return True
print ("Ran")
