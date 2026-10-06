def  verEdad(edad):
    if edad < 18:
        return False
    elif edad >= 18:
        return True
    else:
        return True
    
assert verEdad(18) == True
print("funcion correcta")