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

# Obtener una profesión por idProf
@app.route("/api/profesiones/<string:idProf>", methods=["GET"])
def obtener_profesion_por_idProf(idProf):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM profesionesdb WHERE idProf = %s", (idProf,))
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
        INSERT INTO profesionesdb (id, idProf, nombreProf, descripccion, Fecha, FolioPersonaIne)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    valores = (
        nuevo_id,
        datos.get("idProf"),
        datos.get("nombreProf"),
        datos.get("descripccion"),
        datos.get("Fecha"),
        datos.get("FolioPersonaIne")
    )

    cursor.execute(query, valores)
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Profesión creada", "id": nuevo_id}), 201

# Actualizar una profesión existente por idProf
@app.route("/api/profesiones/<string:idProf>", methods=["PUT"])
def actualizar_profesion(idProf):
    datos = request.get_json()
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        UPDATE profesionesdb
        SET nombreProf = %s, descripccion = %s, Fecha = %s, FolioPersonaIne = %s
        WHERE idProf = %s
    """
    valores = (
        datos.get("nombreProf"),
        datos.get("descripccion"),
        datos.get("Fecha"),
        datos.get("FolioPersonaIne"),
        idProf
    )

    cursor.execute(query, valores)
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Profesión actualizada"})

# Eliminar una profesión por idProf
@app.route("/api/profesiones/<string:idProf>", methods=["DELETE"])
def eliminar_profesion(idProf):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM profesionesdb WHERE idProf = %s", (idProf,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": "Profesión eliminada"})

# Iniciar localmente (no se usa en Render)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
