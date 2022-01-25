import math

AB = int(input())
BC = int(input())

# get hypothenuse, use Pythagorean theorem
h = math.sqrt(AB**2 + BC**2)
CM = h/2

# calculate the angles
A = math.asin(BC/h)
C = math.asin(AB/h)

# find the length of BM, use Cosine rule
BM = math.sqrt(CM**2 + BC**2 - 2*CM*BC*math.cos(C))

# find the angle of B, still Cosine rule
B = math.acos((CM**2 + BC**2 - BM**2)/(2*CM*BC))

print(math.degrees(B))
print(u'\N{DEGREE SIGN}')