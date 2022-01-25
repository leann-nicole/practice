
def make_bricks(small, big, goal):
  if small >= goal:
    return True
  elif not big:
    return False
    
  if big*5 >= goal:
    if goal%5 == 0:
      return True
    if small - (goal%5) >= 0:
      return True
    return False
    
  elif small - (goal - big*5) >= 0:
    return True
  return False

small = int(input("Small: "))
big = int(input("Big: "))
goal = int(input("Goal: "))

print(make_bricks(small, big, goal))