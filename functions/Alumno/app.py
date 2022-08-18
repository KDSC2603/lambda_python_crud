
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

        table = dynamodb.Table('Alumnos')
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
            nombre,table.name,
            err.response['Error']['Code'], err.response['Error']['Message'])
        raise
def lambda_handler(event,context):
    logger.info("evento: "+event)

    body=json.loads(event)
    id_alumno=body["id_alumno"]
    nombre=body["nombre"]
    apellido=body["apellido"]
    curso=body["curso"]
    direccion=body["direccion"]
    edad=body["edad"]
    estado=body["estado"]
    fecha_nacimiento=body["fecha_nacimiento"]
    genero=body["genero"]

    add_alumnos(id_alumno, nombre, apellido, curso, direccion, edad, estado, fecha_nacimiento, genero)