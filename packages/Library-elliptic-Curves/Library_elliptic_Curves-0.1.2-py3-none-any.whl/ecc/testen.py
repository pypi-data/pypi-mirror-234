import Kurven as curves
import elliptischeKurve as eK
import endlicheKoerper_Fp as eG
import endlicherKoerper_F2n as di_n
import endlicherKoerper_Fpn as poly_n
import math
import copy
import random
import Kurven
import Menezes_vanstone_Ascii  as Mv


'innit'
Kurve = curves.Ascii()
startpunkt = Kurve.startpoint

privatekeya = random.randrange(int(Kurve.bound()[0]))
publickey_ga = startpunkt * privatekeya

'decribtion'
text = "test test 123 auch ueber 16 stellen"
totalmessage = Mv.text_to_ascii(text)
message = totalmessage[0]
print(message)
print("")
encrypted = Mv.Menezes_Vanstone_encrybtion(message,Kurve,publickey_ga)[0]
print(encrypted)
print("")
decrypted = Mv.Menezes_Vanstone_decrybtion(encrypted, Kurve, privatekeya)
#print(encrypted)
print("")
textdecripted= Mv.ascii_to_text(decrypted)
print(textdecripted)