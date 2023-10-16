from .Kurven import Ascii
import random
from .Menezes_vanstone_Ascii import text_to_ascii, ascii_to_text, Menezes_Vanstone_decrybtion,Menezes_Vanstone_encrybtion


'innit'
Kurve = Ascii()
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