from .elliptischeKurve import curve_Fpn

Kurve = curve_Fpn([10, 5, 8, 4, 0, 8, 6],[9, 2, 3, 8, 1, 10, 1],11,[1, 10, 3, 7, 6, 6, 3, 6],[[10, 5, 5, 7, 4, 5, 10],[5, 9, 2, 2, 0, 7, 1]],None)
Punkt = Kurve.startpoint
print(Punkt)
a = Punkt.invminus()
print(a, a.on_Curve())