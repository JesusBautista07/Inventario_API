import requests

BASE_URL = "http://127.0.0.1:5000"


def mostrar_producto(producto):
    print(f"  ID: {producto['id']} | {producto['nombre']} | "
          f"${producto['precio']} | Cantidad: {producto['cantidad']} | "
          f"Categoria: {producto['categoria']}")


def listar_prod():
    respuesta = requests.get(f"{BASE_URL}/productos")
    if respuesta.status_code == 200:
        datos = respuesta.json()
        print("\n--- Lista de productos ---")
        for producto in datos:
            mostrar_producto(producto)
    else:
        print("Ocurrio un problema al listar los productos.")


def consultar_prod_id():
    id_producto = input("Ingrese el ID del producto: ")
    respuesta = requests.get(f"{BASE_URL}/productos/{id_producto}")

    if respuesta.status_code == 200:
        producto = respuesta.json()
        print("\n--- Producto encontrado ---")
        mostrar_producto(producto)

    elif respuesta.status_code == 404:
        print("Producto no encontrado.")

    else:
        print("Ocurrió un error.")


def agregar_prod():
    print("\n--- Ingresa los datos del nuevo producto ---")
    nombre = input("Nombre: ")
    precio = float(input("precio: "))
    cantidad = int(input("cantidad: "))
    categoria = input("categoria: ")

    nuevo_prod = {
        'nombre': nombre,
        'precio': precio,
        'cantidad': cantidad,
        'categoria': categoria
    }

    respuesta = requests.post(f"{BASE_URL}/productos", json=nuevo_prod)

    if respuesta.status_code == 201:
        producto = respuesta.json()
        print("\nProducto creado:")
        mostrar_producto(producto)
    elif respuesta.status_code == 400:
        print("Datos inválidos.")
    else:
        print("Ocurrió un error.")


def modificar_prod():
    id_producto = int(input("Que ID deseas modificar: "))

    print("\n--- Ingresa los nuevos datos ---")
    nombre = input("Nombre: ")
    precio = float(input("precio: "))
    cantidad = int(input("cantidad: "))
    categoria = input("categoria: ")

    modificado_prod = {
        'nombre': nombre,
        'precio': precio,
        'cantidad': cantidad,
        'categoria': categoria
    }

    respuesta = requests.put(f"{BASE_URL}/productos/{id_producto}", json=modificado_prod)

    if respuesta.status_code == 200:
        producto = respuesta.json()
        print("\nProducto modificado correctamente:")
        mostrar_producto(producto)
    elif respuesta.status_code == 404:
        print("producto no encontrado")
    else:
        print("Ocurrio un error.")


def eliminar_prod():
    id_producto = int(input("Que ID deseas eliminar: "))
    respuesta = requests.delete(f"{BASE_URL}/productos/{id_producto}")

    if respuesta.status_code == 200:
        resultado = respuesta.json()
        print(resultado["mensaje"])

    elif respuesta.status_code == 404:
        print("producto no encontrado")
    else:
        print("Ocurrio un error.")


def buscar_prod_nombre():
    buscar_nombre = input("Que nombre deseas buscar: ")
    respuesta = requests.get(f"{BASE_URL}/productos/buscar/{buscar_nombre}")

    if respuesta.status_code == 200:
        productos = respuesta.json()

        if not productos:
            print("No se encontraron productos con ese nombre.")
        else:
            print("\n--- Resultados de la búsqueda ---")
            for producto in productos:
                mostrar_producto(producto)


def buscar_bajo_stock():
    respuesta = requests.get(f"{BASE_URL}/productos/bajo-stock")

    if respuesta.status_code == 200:
        productos = respuesta.json()

        if not productos:
            print("No hay productos con bajo stock.")
        else:
            print("\n--- Productos con bajo stock ---")
            for producto in productos:
                mostrar_producto(producto)


while True:
    print("\n===== MENÚ INVENTARIO =====")
    print("1. Listar productos")
    print("2. Consultar producto por ID")
    print("3. Agregar producto")
    print("4. Modificar producto")
    print("5. Eliminar producto")
    print("6. Buscar producto por nombre")
    print("7. Consultar productos con bajo stock")
    print("8. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        listar_prod()
    elif opcion == "2":
        consultar_prod_id()
    elif opcion == "3":
        agregar_prod()
    elif opcion == "4":
        modificar_prod()
    elif opcion == "5":
        eliminar_prod()
    elif opcion == "6":
        buscar_prod_nombre()
    elif opcion == "7":
        buscar_bajo_stock()
    elif opcion == "8":
        print("Saliendo...")
        break
    else:
        print("Opción no válida.")