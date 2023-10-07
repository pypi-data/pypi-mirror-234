import Kurven as curves
import elliptischeKurve as eG
import endlicherKoerper_Fpn as poly_n
import elliptischeKurve as eK
import random
import find_irreducible_polynomial as fip


def get_randomcurve(p, n, should_print = "yes"):

    if isinstance(n,int):
        ir_poly = fip.get_irreductible_polynomial(p,n)[0]
    else:
        ir_poly = n
    x =[]
    for i in range(len(ir_poly)-1):
        x += [random.randrange(p)]
    y =[]
    for i in range(len(ir_poly)-1):
        y += [random.randrange(p)]
    a =[]
    for i in range(len(ir_poly)-1):
        a += [random.randrange(p)]
    temp_b = [0]
    Kurve = eG.curve_Fpn(a,temp_b,p,ir_poly,[x,y],None)
    leftandright = Kurve.compute(x,y)
    b = (poly_n.Fpn(p, ir_poly, leftandright[0]) - poly_n.Fpn(p, ir_poly,  leftandright[1])).value
    curve =(eK.curve_Fpn(a,b,p,ir_poly,[x,y],None))
    if curve.discriminante_is_zero():
        return get_randomcurve(p,n,should_print)
    if not curve.startpoint.on_Curve:
        print("Fehler beim erstellen.")
    if should_print == "yes":            
        print("irreduzibles Polynom = ", ir_poly)
        print("a = ", a)
        print("b = ", b)
        print("x = ", x)
        print("y = " ,y)
        print("Kurve wurde erfolgreich generiert. Hier die Kurve um abzuspeichern.")
        print(f"Kurve = eG.curve_Fpn({a},{b},{p},{ir_poly},[{x},{y}],None)")
    return curve