import Kurven as curves
import copy
import elliptischeKurve as eK
import endlicheKoerper_Fp as eG
import endlicherKoerper_F2n as di_n
import endlicherKoerper_Fpn as poly_n
import math
import random
import time
p = 999999999989
ir_poly = [1, 796165772192, 829481024124, 173348539812, 664891732825, 634326875814, 47914038765, 984700663244, 173061265770, 467219044206, 572605461730, 514511840685, 397768102575, 42384905141, 166305160910, 306798554646, 124757603529, 138438348900, 277665291086, 605079768851, 160902066182]


a = poly_n.Fpn(p,ir_poly,[997599950375, 355623952961, 997340455532, 588334145012, 252452736358, 247234254166, 499281407142, 681759957398, 764723568447, 117950226196, 392668655754, 
212874702043, 704000223873, 332677307950, 717103418846, 899146630732, 543357392736, 704663648497, 530038209737, 943142709496])
print(a)
b = ~a
print(b)
k = 1


start_proc = time.process_time()

for i in range(k):
    b = ~a
ende_proc = time.process_time()
print('Systemzeit: {:5.3f}s'.format(ende_proc-start_proc))
print(b*a)
start_proc = time.process_time()
for i in range (k):
    s = a ** p
    f = (a.degree * (a.degree+1)) //2
    s = s**f
    t = s * a
    inverse = pow(t.value[-1],-1,p)
    b2 = s * poly_n.Fpn(p, ir_poly,[inverse])
ende_proc = time.process_time()
print('Systemzeit: {:5.3f}s'.format(ende_proc-start_proc))
print(b2*a)