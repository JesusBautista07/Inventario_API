def calcularDescuento(precio, rorcentaje):
    descuento = precio * rorcentaje / 100
    precio = precio - descuento
    return precio

assert calcularDescuento(100000, 10) == 90000

print("funcion correcta")