# Perú - UBIGEO 2002
## Escenario
El ubigeo es el código de ubicación geográfica en Perú, un código de seis cifras que identifica de manera única cada departamento, provincia y distrito del país.

El código se organiza de la siguiente manera: 
* Dos dígitos: para el departamento.
* Dos dígitos: para la provincia.
* Dos dígitos: para el distrito.

Se tiene dos archivos con información del UBIGEO del año 2002, con el siguiente detalle:
* __ubigeo2002.DBF__: Departamentos, provincias y distritos.
* __ccpp2002.DBF__: Centros poblados. Incluye la clasificación, el número aprpximado de viviendas y la categoría del centro poblado.

El proyecto trata de trasladar esta información, contenida en los archivos DBF, al data lake, considerando los siguientes pasos:
* Copiar los archivos DBF desde la computadora con WSL (WSL-MOYOBAMBA) hacia el nodo principal del cluster (lluyllucucha)
* Convertir la información de los archivos DBF a archivos CSV.
* Con Spark, realizar lo siguiente:
  - Crear la base de datos __ubigeo__ en el metastore de Hive.
  - En la base de datos __ubigeo__, crear las tablas externas en formato parquet __bronze_ubigeo2002__ y __bronze_ccpp2002__.
* Con Spark, usando las tablas __bronze_ubigeo2002__ y __bronze_ccpp2002__, en la base de datos __ubigeo__ crear las siguientes tablas externas en formato parquet:
  - __silver_departamentos2002__: Departamentos al año 2002
  - __silver_provincias2002__: Provincias al año 2002
  - __silver_distritos2002__: Distritos al año 2002
  - __silver_centrospoblados2002__: Centros poblados al año 2002
  - __silver_categorias2002__: Categorías de centros poblados al año 2002

La ubicación de las tablas externas serán las siguientes:
* __/dtlk/data/bronze/<nombre_proyecto>/<nombre_tabla>/external__: Para las tablas en la capa bronze
* __/dtlk/data/silver/<nombre_proyecto>/<nombre_tabla>/external__: Para las tablas en la capa silver
* __/dtlk/data/gold/<nombre_proyecto>/<nombre_tabla>/external__: Para las tablas en la capa gold
