client_2 = {"hello":1,"now":2,"good":3,"keep":4,"nice":5}
name = "Direct: (hello,now , good , keep , nice ) Hello how are U?" 
names = name[name.find("(") + 1 : name.find(")")]
print(names)
names = names.split(",")
print(names)
names = list(map(str.strip,names))
print(names)
names = list(map(lambda x: client_2[x],names))
print(names)

