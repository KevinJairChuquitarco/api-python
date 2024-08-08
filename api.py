from flask import Flask, request, jsonify 
import psycopg2
from flask_cors import CORS

#creo una variable conexión
conn = psycopg2.connect(host="localhost",database="zoodb",user="postgres",password="123456")
cur = conn.cursor()

app = Flask(__name__)
CORS(app)

respuesta = { "datos":[],"estado":200,"mensaje":"Bienvenido" }

#ruta de bienvenida
@app.route("/")
def bienvenida():
    respuesta["datos"]=""
    respuesta["estado"]=200
    respuesta["mensaje"]="Bienvenido a la aplicación"
    return jsonify(respuesta)

#Función para obtener todos los animales
@app.route("/animales",methods=["GET"])
def obtenerAnimales():
    try:
        cur.execute("Select *From animal")
        animales = cur.fetchall()
        animalesjson = [{"id":animal[0],"nombre":animal[1],"urlimagen":animal[2]
                     ,"descripcion":animal[3],"id_categoria":animal[4]} 
                     for animal in animales]
        respuesta["datos"]=animalesjson
        respuesta["estado"]=200
        respuesta["mensaje"]="Los animales se obtuvieron correctamente"
    except:
        respuesta["datos"]=""
        respuesta["estado"]=500
        respuesta["mensaje"]="Ocurrió un error en obtener datos"
    return jsonify(respuesta)
    
    

#Obtener un sólo animal
@app.route("/animales/<int:id>",methods=["GET"])
def obtenerAnimal(id):
    try: 
        cur.execute("Select *From animal where id = %s",(id,))
        animal = cur.fetchone()
        animalesjson = {"id":animal[0],"nombre":animal[1],"urlimagen":animal[2]
                        ,"descripcion":animal[3],"id_categoria":animal[4]}
        respuesta["datos"]=animalesjson
        respuesta["estado"]=200
        respuesta["mensaje"]="Animal obtenido correctamente" 
    except:
        respuesta["datos"]=""
        respuesta["estado"]=500
        respuesta["mensaje"]="Ocurrió un error en obtener datos"
    return jsonify(respuesta)

#Creo un nuevo animal
@app.route("/animales",methods=["POST"])
def crearAnimal():
    try:
        atributos = request.get_json()
        nombre = atributos.get("nombre")
        url = atributos.get("urlimagen")
        descripcion = atributos.get("descripcion")
        idCategoria = atributos.get("id_categoria")
        cur.execute("Insert into animal (nombre,urlimagen,descripcion,id_categoria) values (%s,%s,%s,%s) RETURNING id"
                    ,(nombre,url,descripcion,idCategoria))
        idAnimal =  cur.fetchone()[0]
        conn.commit()
        animalNuevo = {"id":idAnimal,"nombre":nombre,"urlimagen":url
                        ,"descripcion":descripcion,"id_categoria":idCategoria}
        respuesta["datos"]=animalNuevo
        respuesta["estado"]=200
        respuesta["mensaje"]="Animal creado correctamente" 
    except:
        respuesta["datos"]=""
        respuesta["estado"]=500
        respuesta["mensaje"]="Ocurrio un error al crear el animal" 
    return jsonify(respuesta)
#función para actualizar un animal
@app.route("/animales",methods=["PUT"])
def actualizarAnimal():
    try:
        atributos = request.get_json()
        id = atributos.get("id")
        nombre = atributos.get("nombre")
        url = atributos.get("urlimagen")
        descripcion = atributos.get("descripcion")
        idCategoria = atributos.get("id_categoria")
        cur.execute("Update animal Set nombre=%s,urlimagen=%s,descripcion = %s, id_categoria=%s Where id = %s"
                    ,(nombre,url,descripcion,idCategoria,id))
        conn.commit()
        animalActualizado = {"id":id,"nombre":nombre,"urlimagen":url
                        ,"descripcion":descripcion,"id_categoria":idCategoria}
        respuesta["datos"]=animalActualizado
        respuesta["estado"]=200
        respuesta["mensaje"]="Ocurrio un error al crear el animal" 
    except:
        respuesta["datos"]=""
        respuesta["estado"]=500
        respuesta["mensaje"]="Ocurrio un error al actualizar el animal" 

    return jsonify(respuesta)

#función para elminiar un animal
@app.route("/animales/<int:id>",methods=["DELETE"])
def eliminarAnimal(id):
    try:
        cur.execute("Delete from animal where id = %s",(id,))
        conn.commit()
        respuesta["datos"]={"id":id}
        respuesta["estado"]=200
        respuesta["mensaje"]="Animal eliminado correctamente" 
    except:
        respuesta["datos"]=""
        respuesta["estado"]=500
        respuesta["mensaje"]="Ocurrio un error al eliminar el animal" 
    return jsonify(respuesta)

#inicia el servidor
if __name__ == "__main__":
    app.run(debug=True)