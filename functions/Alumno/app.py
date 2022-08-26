
from audioop import add
import json
from pprint import pprint
import boto3
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def add_alumnos(id_alumno, nombre, apellido, curso, direccion, edad, estado, fecha_nacimiento, genero):
    try:
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb')

        table = dynamodb.Table('Alumno')
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

        
        
def get_alumnos(id_alumno, nombre):
    try:
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

    body=event
    id_alumno = body["id_alumno"]
    nombre = body["nombre"]
    #apellido = body["apellido"]
    
    #curso = body["curso"]
    #direccion = body["direccion"]
    #edad = body["edad"]
    #estado = body["estado"]
    #fecha_nacimiento = body["fecha_nacimiento"]
    #genero = body["genero"]
    #add_alumnos(id_alumno, nombre, apellido, curso, direccion, edad, estado, fecha_nacimiento, genero)
    #update_alumnos(id_alumno, nombre, apellido, curso, direccion, edad, estado, fecha_nacimiento, genero)
    delete_alumnos(id_alumno, nombre)
    #get_alumnos(id_alumno,nombre)

# if __name__ == '__main__':
#     update_response = update_alumnos(
#     7, "Juan", "Flores", "Computacion", "av.fresas", 28, "activo", "26-03-2012", "Masculino")
#     print("Update movie succeeded:")
#     pprint(update_response, sort_dicts