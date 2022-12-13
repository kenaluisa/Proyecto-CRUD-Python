from flask import Flask ,jsonify ,request
# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app=Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend
# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/proyectofinal'
# desde el objeto app configuro la URI de la BBDD    user:clave@localhost/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)
ma=Marshmallow(app)
 
# defino la tabla
class Receta(db.Model):   # la clase Producto hereda de db.Model     
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    nombre=db.Column(db.String(100))
    imagen=db.Column(db.String(1000))
    descripcion=db.Column(db.String(500))
    def __init__(self,nombre,imagen,descripcion):   #crea el  constructor de la clase
        self.nombre=nombre   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.imagen=imagen
        self.descripcion=descripcion
 
 
 
with app.app_context():
    db.create_all()  # crea las tablas
#  ************************************************************
class RecetaSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','imagen','descripcion')
receta_schema=RecetaSchema()            # para crear un producto
recetas_schema=RecetaSchema(many=True)  # multiples registros
 
# crea los endpoint o rutas (json)
@app.route('/recetas',methods=['GET'])
def get_Recetas():
    all_recetas=Receta.query.all()     # query.all() lo hereda de db.Model
    result=recetas_schema.dump(all_recetas)  # .dump() lo hereda de ma.schema
    return jsonify(result)
 
@app.route('/recetas/<id>',methods=['GET'])
def get_receta(id):
    receta=Receta.query.get(id)
    return receta_schema.jsonify(receta)

@app.route('/recetas/<id>',methods=['DELETE'])
def delete_receta(id):
    receta=Receta.query.get(id)
    db.session.delete(receta)
    db.session.commit()
    return receta_schema.jsonify(receta)

@app.route('/recetas', methods=['POST']) # crea ruta o endpoint
def create_receta():
    print(request.json)  # request.json contiene el json que envio el cliente
    nombre=request.json['nombre']
    imagen=request.json['imagen']
    descripcion=request.json['descripcion']
    new_receta=Receta(nombre,imagen,descripcion)
    db.session.add(new_receta)
    db.session.commit()
    return receta_schema.jsonify(new_receta)

@app.route('/recetas/<id>' ,methods=['PUT'])
def update_receta(id):
    receta=Receta.query.get(id)
   
    nombre=request.json['nombre']
    imagen=request.json['imagen']
    descripcion=request.json['descripcion']
 
    receta.nombre=nombre
    receta.imagen=imagen
    receta.descripcion=descripcion
    db.session.commit()
    return receta_schema.jsonify(receta)
 

# programa principal *******************************
if __name__=='__main__':  
    app.run(debug=True, port=5000) 