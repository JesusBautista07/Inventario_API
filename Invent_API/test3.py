def Prom(nt1, nt2, nt3):
    promedio = (nt1 + nt2 + nt3) / 3
    if promedio >= 3:
        return "aprobado"
    elif promedio < 3:
        return "desaprobado"
    
    
assert Prom(2,3,4) == "aprobado"
print("funcion correcta")

