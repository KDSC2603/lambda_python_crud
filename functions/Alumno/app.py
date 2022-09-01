
from audioop import add
import json
from pprint import pprint
import boto3
from botocore.exceptions import ClientError
import logging
from decimal import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def decimal_convert(obj):
    if isinstance(obj, Decimal):
        return str(obj)

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

        rpt="Alumno insertado exitosamente"
        return rpt
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
        rpt="Alumno actualizado exitosamente"
        return rpt
    except ClientError as err:
        logger.exception(err)
        
#Eliminar
def delete_alumnos(id_alumno, nombre):
    logger.info("metodo para eliminar alumno")

    id_alumno=int(id_alumno)
    logger.info("type id_alumno: {} nombre: {}".format(type(id_alumno),type(nombre)))

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

    id_alumno=int(id_alumno)
    logger.info("type id_alumno: {} nombre: {}".format(type(id_alumno),type(nombre)))

    try:
        response=None
        msj=None
        
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('alumno')
        
        
        response = table.get_item(Key={'id_alumno': id_alumno, 'nombre':nombre})

        
        logger.info("response: " + str(response))
    
        item = response.get('Item', None)
    
        return item
    except ClientError as err:
        logger.exception(err)

def lambda_handler(event, context):
    response=None
    msj=None
    logger.info("evento: {}".format(json.dumps(event)))
    
    httpMethod=event.get("httpMethod",None)
    logger.info("httpMethod: {}".format(httpMethod))


    if httpMethod =="POST":
        body = event.get("body",None)
        #TODO revisar cuando body es none
        json_body=json.loads(body)

        id_alumno = json_body.get("id_alumno", None)
        nombre = json_body.get("nombre",None)
        apellido = json_body.get("apellido",None)
        curso = json_body.get("curso",None)
        direccion = json_body.get("direccion",None)
        edad = json_body.get("edad",None)
        estado = json_body.get("estado",None)
        fecha_nacimiento = json_body .get("fecha_nacimiento",None)
        genero = json_body.get("genero",None)

        msj=add_alumnos(id_alumno, nombre, apellido, curso, direccion, edad, estado, fecha_nacimiento, genero)
    elif httpMethod =="GET":
        pathParameters=event.get("pathParameters",None)
        nombre=pathParameters.get("nombre",None)
        id=pathParameters.get("id",None)
        logger.info("pathParameters: {}".format(pathParameters))
        logger.info("nombre: {} id: {}".format(nombre,id))
        msj=get_alumnos(id,nombre)

    elif httpMethod =="DELETE":
        pathParameters=event.get("pathParameters",None)
        nombre=pathParameters.get("nombre",None)
        id=pathParameters.get("id",None)
        logger.info("pathParameters: {}".format(pathParameters))
        logger.info("nombre: {} id: {}".format(nombre,id))
        msj=delete_alumnos(id, nombre)  
    elif httpMethod =="PUT":
        body = event.get("body",None)
        #TODO revisar cuando body es none
        json_body=json.loads(body)

        id_alumno = json_body.get("id_alumno", None)
        nombre = json_body.get("nombre",None)
        apellido = json_body.get("apellido",None)
        curso = json_body.get("curso",None)
        direccion = json_body.get("direccion",None)
        edad = json_body.get("edad",None)
        estado = json_body.get("estado",None)
        fecha_nacimiento = json_body .get("fecha_nacimiento",None)
        genero = json_body.get("genero",None)
        msj=update_alumnos(id_alumno, nombre, apellido, curso, direccion, edad, estado, fecha_nacimiento, genero)
    
    # if operacion=="crear":
    #     msj=add_alumnos(id_alumno, nombre, apellido, curso, direccion, edad, estado, fecha_nacimiento, genero)
    
    # elif operacion=="actualizar":
    #     msj=update_alumnos(id_alumno, nombre, apellido, curso, direccion, edad, estado, fecha_nacimiento, genero)
    
    # elif operacion=="eliminar":
    #     msj=delete_alumnos(id_alumno, nombre)

    # elif operacion=="buscar":
    #     msj=get_alumnos(id_alumno,nombre)
    
    # else:
    #     logger.info("operacion invalida")
    #     msj="operacion invalida"


    response = {
            "statusCode": 200,
            "headers": {
            "Access-Control-Allow-Headers": '*',
            "Access-Control-Allow-Origin": '*',
            "Access-Control-Allow-Methods": '*'
        },
            "body": json.dumps(msj,default=decimal_convert)
        }
    return response
    