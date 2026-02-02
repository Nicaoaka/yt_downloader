import copy
a = [124]
b = []
c = copy.deepcopy(b or a)
print(c)


