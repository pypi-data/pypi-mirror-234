def add(a,b,c=None):

    if c == None:
        return(a+b)
    else:
        return (a+b) % c
    
print(add(5,384))