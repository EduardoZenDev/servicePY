from flask import Flask, request, jsonify
from db import get_connection
import os

app = Flask(__name__)

# Ruta raíz
@app.route("/")
def home():
    return "¡Microservicio de profesiones funcionando!"

# Obtener todas las profesiones
@app.route("/api/profesiones", methods=["GET"])
def obtener_profesiones():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM profesionesdb")
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado)

# Obtener una profesión por ID
@app.route("/api/profesiones/<int:id>", methods=["GET"])
def obtener_profesion_por_id(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM profesionesdb WHERE id = %s", (id,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(resultado or {})

# Crear una nueva profesión
@app.route("/api/profesiones", methods=["POST"])
def crear_profesion():
    datos = request.get_json()
    conn = get_connection()
    cursor = conn.cursor()

    # Obtener el siguiente ID manual
    cursor.execute("SELECT MAX(id) FROM profesionesdb")
    max_id = cursor.fetchone()[0]
    nuevo_id = 1 if max_id is None else max_id + 1

    query = """
        INSERT INTO profesionesdb (id, idProf, nombreProf, descripccion, Fecha)
        VALUES (%s, %s, %s, %s, %s)
    """
    valores = (
        nuevo_id,
        datos.get("idProf"),
        datos.get("nombreProf"),
        datos.get("descripccion"),
        datos.get("Fecha")
    )

    cursor.execute(query, valores)
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Profesión creada", "id": nuevo_id}), 201

# Actualizar una profesión existente
@app.route("/api/profesiones/<int:id>", methods=["PUT"])
def actualizar_profesion(id):
    datos = request.get_json()
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        UPDATE profesionesdb
        SET idProf = %s, nombreProf = %s, descripccion = %s, Fecha = %s
        WHERE id = %s
    """
    valores = (
        datos.get("idProf"),
        datos.get("nombreProf"),
        datos.get("descripccion"),
        datos.get("Fecha"),
        id
    )

    cursor.execute(query, valores)
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Profesión actualizada"})

# Eliminar una profesión
@app.route("/api/profesiones/<int:id>", methods=["DELETE"])
def eliminar_profesion(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM profesionesdb WHERE nombreProf = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": "Profesión eliminada"})

# Iniciar la aplicación localmente (Render usará gunicorn, no esto)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
