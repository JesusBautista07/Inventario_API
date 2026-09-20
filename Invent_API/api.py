from flask import Flask, jsonify, request

app = Flask(__name__)


productos = [
    {"id": 1, "nombre": "Teclado mecánico", "precio": 120000, "cantidad": 10, "categoria": "Periféricos"},
    {"id": 2, "nombre": "Mouse inalámbrico", "precio": 45000, "cantidad": 3, "categoria": "Periféricos"},
    {"id": 3, "nombre": "Monitor 24 pulgadas", "precio": 650000, "cantidad": 5, "categoria": "Monitores"},
]

siguiente_id = 4


def buscar_producto_por_id(producto_id):
    for producto in productos:
        if producto["id"] == producto_id:
            return producto
    return None


def validar_datos_producto(datos, es_actualizacion=False):
    """
    Valida los datos recibidos para crear/modificar un producto.
    Devuelve None si son válidos, o un mensaje de error (string) si no.
    """
    if datos is None:
        return "Los datos deben recibirse en formato JSON"

    campos_requeridos = ["nombre", "precio", "cantidad", "categoria"]
    for campo in campos_requeridos:
        if campo not in datos:
            return f"El campo '{campo}' es obligatorio"

    nombre = datos.get("nombre")
    if not isinstance(nombre, str) or not nombre.strip():
        return "El nombre no puede estar vacío"

    precio = datos.get("precio")
    if not isinstance(precio, (int, float)) or isinstance(precio, bool) or precio <= 0:
        return "El precio debe ser mayor que cero"

    cantidad = datos.get("cantidad")
    if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad < 0:
        return "La cantidad no puede ser negativa"

    categoria = datos.get("categoria")
    if not isinstance(categoria, str) or not categoria.strip():
        return "La categoría no puede estar vacía"

    return None


@app.route("/productos", methods=["GET"])
def obtener_productos():
    return jsonify(productos), 200


@app.route("/productos/<int:producto_id>", methods=["GET"])
def obtener_producto(producto_id):
    producto = buscar_producto_por_id(producto_id)
    if producto is None:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify(producto), 200


@app.route("/productos", methods=["POST"])
def crear_producto():
    global siguiente_id

    if not request.is_json:
        return jsonify({"error": "Los datos deben recibirse en formato JSON"}), 400

    datos = request.get_json(silent=True)
    error = validar_datos_producto(datos)
    if error:
        return jsonify({"error": error}), 400

    nuevo_producto = {
        "id": siguiente_id,
        "nombre": datos["nombre"].strip(),
        "precio": datos["precio"],
        "cantidad": datos["cantidad"],
        "categoria": datos["categoria"].strip(),
    }
    productos.append(nuevo_producto)
    siguiente_id += 1

    return jsonify(nuevo_producto), 201


@app.route("/productos/<int:producto_id>", methods=["PUT"])
def actualizar_producto(producto_id):
    producto = buscar_producto_por_id(producto_id)
    if producto is None:
        return jsonify({"error": "Producto no encontrado"}), 404

    if not request.is_json:
        return jsonify({"error": "Los datos deben recibirse en formato JSON"}), 400

    datos = request.get_json(silent=True)
    error = validar_datos_producto(datos, es_actualizacion=True)
    if error:
        return jsonify({"error": error}), 400

    producto["nombre"] = datos["nombre"].strip()
    producto["precio"] = datos["precio"]
    producto["cantidad"] = datos["cantidad"]
    producto["categoria"] = datos["categoria"].strip()

    return jsonify(producto), 200


@app.route("/productos/<int:producto_id>", methods=["DELETE"])
def eliminar_producto(producto_id):
    producto = buscar_producto_por_id(producto_id)
    if producto is None:
        return jsonify({"error": "Producto no encontrado"}), 404

    productos.remove(producto)
    return jsonify({"mensaje": "Producto eliminado correctamente"}), 200


@app.route("/productos/buscar/<string:nombre>", methods=["GET"])
def buscar_productos(nombre):
    resultado = [
        p for p in productos if nombre.strip().lower() in p["nombre"].lower()
    ]
    return jsonify(resultado), 200


@app.route("/productos/bajo-stock", methods=["GET"])
def productos_bajo_stock():
    resultado = [p for p in productos if p["cantidad"] <= 5]
    return jsonify(resultado), 200


@app.route("/productos/categoria/<string:categoria>", methods=["GET"])
def productos_por_categoria(categoria):
    resultado = [
        p for p in productos if p["categoria"].lower() == categoria.strip().lower()
    ]
    return jsonify(resultado), 200


@app.route("/productos/valor-total", methods=["GET"])
def valor_total_inventario():
    total = sum(p["precio"] * p["cantidad"] for p in productos)
    return jsonify({"valor_total": total}), 200


@app.errorhandler(404)
def ruta_no_encontrada(e):
    return jsonify({"error": "Ruta no encontrada"}), 404


@app.errorhandler(405)
def metodo_no_permitido(e):
    return jsonify({"error": "Método no permitido"}), 405


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)