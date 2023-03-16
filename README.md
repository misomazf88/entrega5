# Entrega 5

Repositorio con código base para la implementación de 3 microservicios comunicandose por medio de comandos y eventos, se creo Backend for Frontend (BFF) usando GraphQL como lenguaje de creacion de comandos y consultas hacia aplicacion flask alpesonline quien a su vez hacer de saga con orquestacion para manejo de atomicidad en una transaccion entre los 3 microservicios desarrollados.


## Estructura del proyecto

Este repositorio tiene la siguiente estructura:

- El directorio src/integracion_logistica/ ahora incluye todas las clases y archivos que constituyen el contexto con la integración con logistica.
- El directorio src/inventario/ ahora incluye todas las clases y archivos que constituyen el contexto de inventario.
- El proyecto alpesonline ahora cuenta con un nuevo módulo para el manejo de sagas src/alpesonline/modulos/sagas/.
- Módulo aplicacion que cuenta con código de los comandos para múltiples contextos fuera del de ordenes.
- Módulo coordinadores que cuenta con la saga de ordenes usando orquestación.
- Los archivos src/alpesonline/seedwork/aplicacion/sagas.py provee las interfaces y definiciones genéricas para la coordinación de sagas.
- El directorio **src/bff_web/** incluye el código del BFF Web. Este servicio cuenta con la siguiente estructura:
    - **consumidores**: Código con la lógica para leer y procesar eventos del broker de eventos.
    - **despachadores**: Código con la lógica para publicar comandos al broker de eventos.
    - **main**: Archivo con la lógica de despliegue y configuración del servidor.
    - **api**: Módulo con la diferentes versiones del API, routers, esquemas, mutaciones y consultas.
- El directorio **src/ui/** cuenta ahora solo con código HTML, estilos CSS y JS. 

## AlpesOnline
### Ejecutar Base de datos
Desde el directorio principal ejecute el siguiente comando.

```bash
docker-compose --profiles db up
```

Este comando descarga las imágenes e instala las dependencias de la base datos.

### Ejecutar Aplicación

Desde el directorio principal ejecute el siguiente comando.

```bash
flask --app src/alpesonline/api run
```

Siempre puede ejecutarlo en modo DEBUG:

```bash
flask --app src/alpesonline/api --debug run
```

### Ejecutar pruebas

```bash
coverage run -m pytest
```

### Ver reporte de covertura
```bash
coverage report
```

### Crear imagen Docker

Desde el directorio principal ejecute el siguiente comando.

```bash
docker build . -f alpesonline.Dockerfile -t alpesonline/flask
```

### Ejecutar contenedora (sin compose)

Desde el directorio principal ejecute el siguiente comando.

```bash
docker run -p 5000:5000 alpesonline/flask
```

### Compilación gRPC

Desde el directorio `src/sidecar` ejecute el siguiente comando.

```bash
python -m grpc_tools.protoc -Iprotos --python_out=./pb2py --pyi_out=./pb2py --grpc_python_out=./pb2py protos/ordenes.proto
```

### Crear imagen Docker

Desde el directorio principal ejecute el siguiente comando.

```bash
docker build . -f adaptador.Dockerfile -t alpesonline/adaptador
```

### Ejecutar contenedora (sin compose)

Desde el directorio principal ejecute el siguiente comando.

```bash
docker run -p 50051:50051 alpesonline/adaptador
```

## Microservicio: Inventario

Desde el directorio `src` ejecute el siguiente comando

```bash
uvicorn inventario.main:app --host localhost --port 8001 --reload
```

## Microservicio: Integración Logistica

Desde el directorio `src` ejecute el siguiente comando

```bash
uvicorn integracion_Logistica.main:app --host localhost --port 8002 --reload
```

## BFF: Web

Desde el directorio `src` ejecute el siguiente comando

```bash
uvicorn bff_web.main:app --host localhost --port 8003 --reload
```

url para consumo desde navegador:

POST
http://lbn-dermo-app-web-84168d11e474aa03.elb.us-east-1.amazonaws.com:3000/order

GET
http://lbn-dermo-app-web-84168d11e474aa03.elb.us-east-1.amazonaws.com:3000/orders

### Crear imagen Docker

Desde el directorio principal ejecute el siguiente comando.

```bash
docker build . -f ui.Dockerfile -t alpesonline/bff
```

### Ejecutar contenedora (sin compose)

Desde el directorio principal ejecute el siguiente comando.

```bash
docker run alpesonline/bff
```

## CDC & Debezium

**Nota**: Antes de poder ejectuar todos los siguientes comandos DEBE tener la base de datos MySQL corriendo.

### Descargar conector de Debezium

```
wget https://archive.apache.org/dist/pulsar/pulsar-2.10.1/connectors/pulsar-io-debezium-mysql-2.10.1.nar
```

### Ejecutar Debezium
Abrir en una terminal:

```bash
docker exec -it broker bash
```

Ya dentro de la contenedora ejecute:
```bash
./bin/pulsar-admin source localrun --source-config-file /pulsar/connectors/debezium-mysql-source-config.yaml --destination-topic-name debezium-mysql-topic
```

### Consumir eventos Debezium

Abrir en una terminal:

```bash
docker exec -it broker bash
```

Ya dentro de la contenedora ejecute:

```bash
./bin/pulsar-client consume -s "sub-datos" public/default/alpesonlinedb.ordenes.usuarios_legado -n 0
```

### Consultar tópicos
Abrir en una terminal:

```bash
docker exec -it broker bash
```

Ya dentro de la contenedora ejecute:

```bash
./bin/pulsar-admin topics list public/default
```

### Cambiar retención de tópicos
Abrir en una terminal:

```bash
docker exec -it broker bash
```
Ya dentro de la contenedora ejecute:

```bash
./bin/pulsar-admin namespaces set-retention public/default --size -1 --time -1
```

Para poder ver que los cambios fueron efectivos ejecute el siguiente comando:

```bash
./bin/pulsar-admin namespaces get-retention public/default
```

**Nota**: Esto nos dejará con una retención infinita. Sin embargo, usted puede cambiar la propiedad de `size` para poder usar [Tiered Storage](https://pulsar.apache.org/docs/2.11.x/concepts-tiered-storage/)

### Instrucciones oficiales

Para seguir la guía oficial de instalación y uso de Debezium en Apache Pulsar puede usar el siguiente [link](https://pulsar.apache.org/docs/2.10.x/io-cdc-debezium/)


## Docker-compose

Para desplegar toda la arquitectura en un solo comando, usamos `docker-compose`. Para ello, desde el directorio principal, ejecute el siguiente comando:

```bash
docker-compose up
```

Si desea detener el ambiente ejecute:

```bash
docker-compose stop
```

En caso de querer desplegar dicha topología en el background puede usar el parametro `-d`.

```bash
docker-compose up -d
```

## Comandos útiles

### Listar contenedoras en ejecución
```bash
docker ps
```

### Listar todas las contenedoras
```bash
docker ps -a
```

### Parar contenedora
```bash
docker stop <id_contenedora>
```

### Eliminar contenedora
```bash
docker rm <id_contenedora>
```

### Listar imágenes
```bash
docker images
```

### Eliminar imágenes
```bash
docker images rm <id_imagen>
```

### Acceder a una contendora
```bash
docker exec -it <id_contenedora> sh
```

### Kill proceso que esta usando un puerto
```bash
fuser -k <puerto>/tcp
```

### Correr docker-compose usando profiles
```bash
docker-compose --profile <pulsar|alpesonline|ui|notificacion> up
```
