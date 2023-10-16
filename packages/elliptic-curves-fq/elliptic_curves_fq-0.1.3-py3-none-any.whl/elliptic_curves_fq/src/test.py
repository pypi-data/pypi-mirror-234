import copy
from .elliptischeKurve import curve_Fpn, Points, on_Curve
from .endlicherKoerper_Fpn import Fpn
import math
import random

p = 5
poly = [1,3,2,3]
a = [random.randrange(p) for i in range(len(poly)-1)]
print (a)
b = [random.randrange(p) for i in range(len(poly)-1)]
print(b)
Point= [[1,2,4],[1,3,2]]
kurz = curve_Fpn(a,b,p,poly,Point,None)

L = [["inf"]]

for i in range(p):
    for j in range(p):
        #print(j)
        for k in range (p):
            x = [i,j,k]
            for l in range(p):
                for m in range(p):
                    for n in range(p):
                        y =  [l,m,n]
                        Punkt = Points([x,y],kurz)
                        if on_Curve(Punkt,kurz):
                            L.append(Punkt)
print(len(L))
#print (L[75].x.value,L[75].y.value)


                        





#c = kurz.startpoint()
#print(c)
#d = c.generate()
#print (len(d),d[0],d[-1])