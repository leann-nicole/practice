try:
    print(x)
except NameError:
    print("Name error found")
except:
    print("There was an error")
else:
    print("Everything went well")
finally:
    print("We're done")