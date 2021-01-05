x = 0
y =1
z =2
a = False
b= False
c= False
while True:
    if x%4 == 0:
        a = True
    if y%9 == 0:
        b = True
    if z%25 == 0:
        c = True
    if a == True and b == True and c == True:
        print(x,y,z)
        break
    x +=1
    y +=1
    z +=1
    a = False
    b= False
    c= False
        