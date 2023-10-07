import Kurven as curves
import copy
import elliptischeKurve as eK
import endlicheKoerper_Fp as eG
import endlicherKoerper_F2n as di_n
import endlicherKoerper_Fpn as poly_n
import math
import random

p = 5
poly = [1,3,2,3]
a = poly_n.Fpn(p,poly,[random.randrange(p) for i in range(len(poly)-1)])
print (a.value)
b =  poly_n.Fpn(p,poly,[random.randrange(p) for i in range(len(poly)-1)])
print(b.value)
Point= [[1,2,4],[1,3,2]]
kurz = eK.curve(a,b,poly,Point,None)

L = [["inf"]]

for i in range(p):
    for j in range(p):
        #print(j)
        for k in range (p):
            x =  poly_n.Fpn(p,poly,[i,j,k])
            for l in range(p):
                for m in range(p):
                    for n in range(p):
                        y =  poly_n.Fpn(p,poly,[l,m,n])
                        Punkt = eK.Points([x,y],kurz)
                        if eK.on_Curve(Punkt,kurz):
                            L.append(Punkt)
print(len(L))
#print (L[75].x.value,L[75].y.value)


                        





#c = kurz.startpoint()
#print(c)
#d = c.generate()
#print (len(d),d[0],d[-1])