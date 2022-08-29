
from audioop import add
import json
from pprint import pprint
import boto3
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


logger = logging.getLogger()
logger.setLevel(logging.INFO)
#Agregar
def add_alumnos(id_alumno, nombre, apellido, curso, direccion, edad, estado, fecha_nacimiento, genero):
    logger.info("metodo para agregar alumno")
    try:  
        dynamodb = boto3.resource('dynamodb')

        table = dynamodb.Table('alumno')
        response = table.put_item(
            Item={
                'id_alumno': id_alumno,
                'nombre': nombre,
                'apellido': apellido,
                'curso': curso,
                'direccion': direccion,
                'edad':  edad,
                'estado': estado,
                'fecha_nacimiento': fecha_nacimiento,
                'genero':  genero,
            })
        return response
    except ClientError as err:
        

        logger.error(
            "Couldn't add movie %s to table %s. Here's why: %s: %s",
            nombre, table.name,
            err.response['Error']['Code'], err.response['Error']['Message'])
        raise

    #Actualiza
def update_alumnos(id_alumno, nombre, apellido, curso, direccion, edad, estado, fecha_nacimiento, genero):
    logger.info("metodo para actualizar alumno")
    try:

        dynamodb = boto3.resource('dynamodb')

        table = dynamodb.Table('alumno')
        
        response = table.update_item(
          Key={
            'id_alumno': id_alumno,
            'nombre': nombre
        },
            UpdateExpression="set apellido=:a, curso=:c, direccion=:d, edad=:e, estado=:es, fecha_nacimiento=:fn, genero=:g",
            ExpressionAttributeValues={  
                ':a': apellido,
                ':c': curso,
                ':d': direccion,
                ':e': edad,
                ':es': estado,
                ':fn': fecha_nacimiento,
                ':g': genero,
            },
            ReturnValues="UPDATED_NEW"
        )
        return response
    except ClientError as err:
        logger.exception(err)
        
  #Eliminar
def delete_alumnos(id_alumno, nombre):
    logger.info("metodo para eliminar alumno")
    try:
        response=None
        mensaje=None
        dynamodb = boto3.resource('dynamodb')
      
        table = dynamodb.Table('alumno')
        
        item=get_alumnos(id_alumno, nombre)
        
        if item is None:
            mensaje = " El id: " + str(id_alumno)+ " no existe con el nombre " + nombre
            
            response={"message":mensaje }
            
            
        else:
            mensaje = " El id: "+ str(id_alumno)+ "se elimino correctamente con el nombre " +nombre
            table.delete_item(
            Key={
            'id_alumno': id_alumno,
            'nombre': nombre
        })
        response = {"message":mensaje}
        logger.info(response)
      
        return response
    except ClientError as err:
        logger.exception(err)
        
    
#Buscar
def get_alumnos(id_alumno, nombre):
    logger.info("metodo para buscar alumno")
    try:
        response=None
        msj=None
        
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('alumno')
        
        
        response = table.get_item(Key={'id_alumno': id_alumno, 'nombre':nombre
        })
        logger.info("response: " + str(response))
    
        item = response.get('Item', None)
    
        return item
    except ClientError as err:
        logger.exception(err)

def lambda_handler(event, context):
    
    logger.info("evento: "+json.dumps(event))
    
    operacion=event.get("operacion",None)
    data=event.get("data",None)

    id_alumno = data.get("id_alumno", None)
    nombre = data.get("nombre",None)
    apellido = data.get("apellido",None)
    curso = data.get("curso",None)
    direccion = data.get("direccion",None)
    edad = data.get("edad",None)
    estado = data.get("estado",None)
    fecha_nacimiento = data.get("fecha_nacimiento",None)
    genero = data.get("genero",None)
    

    if operacion=="crear":
        add_alumnos(id_alumno, nombre, apellido, curso, direccion, edad, estado, fecha_nacimiento, genero)
    
    elif operacion=="actualizar":
        update_alumnos(id_alumno, nombre, apellido, curso, direccion, edad, estado, fecha_nacimiento, genero)
    
    elif operacion=="eliminar":
        delete_alumnos(id_alumno, nombre)

    elif operacion=="buscar":
        get_alumnos(id_alumno,nombre)
    
    else:
        logger.info("operacion invalida")
    