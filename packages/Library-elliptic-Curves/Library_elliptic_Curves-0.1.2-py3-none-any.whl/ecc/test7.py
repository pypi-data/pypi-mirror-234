import endlicheKoerper_Fp as eK
import elliptischeKurve as eG
import getrandomcurve
i=0
max = 0
while True:
    i+=1
    Kurve = getrandomcurve.get_randomcurve(7,5,"no")
    Punkt = Kurve.startpoint
    a =len(Punkt.generate())
    if a >max:
        max = a
    if i%1000 ==0:
        break
print(max)