names = ["hello" , '', " "]
names = list(filter(lambda x: len(x) != 0 ,names))
print(names)
