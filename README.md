# Documentación: Docker Compose para Elasticsearch y Kibana

## Introducción

Este documento describe la configuración de un entorno basado en Docker Compose para desplegar Elasticsearch y Kibana. Se detallará qué son estos servicios, cómo trabajan juntos y cómo se implementan a través del archivo `docker-compose.yml`.

## ¿Qué es Elasticsearch?

Elasticsearch es un motor de búsqueda y análisis de datos distribuido y en tiempo real basado en Apache Lucene. Es ampliamente utilizado para indexar, buscar y analizar grandes volúmenes de datos de manera rápida y escalable. Entre sus características principales se incluyen:

- Búsqueda y análisis en tiempo real.
- Capacidad de manejar grandes volúmenes de datos.
- Escalabilidad horizontal mediante clustering.
- APIs RESTful para interacción con datos.

## ¿Qué es Kibana?

Kibana es una herramienta de visualización de datos diseñada para trabajar con Elasticsearch. Permite explorar, visualizar y analizar los datos indexados en Elasticsearch a través de gráficos, dashboards interactivos y filtros avanzados. Sus principales características incluyen:

- Visualización de datos en tiempo real.
- Creación de dashboards interactivos.
- Análisis avanzado mediante filtros y agregaciones.
- Integración con Elasticsearch para monitoreo y análisis de logs.

## Relación entre Elasticsearch y Kibana

Kibana se conecta a Elasticsearch para obtener, visualizar y analizar los datos indexados. Elasticsearch actúa como el backend que almacena y procesa los datos, mientras que Kibana proporciona la interfaz de usuario para interactuar con ellos. La integración de ambos permite una gestión eficiente de logs, análisis de tendencias y monitoreo en tiempo real de sistemas y aplicaciones.

## Configuración en Docker Compose

El siguiente archivo `docker-compose.yml` define un entorno con Elasticsearch y Kibana:

```yaml
docker-compose.yml
version: '3.8'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.10.2
    container_name: elasticsearch
    environment:
      - discovery.type=single-node  # Configuración para un solo nodo
      - xpack.security.enabled=false  # Deshabilita la seguridad para simplificar la configuración
    ports:
      - '9200:9200'  # Puerto de la API REST de Elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:8.0.0
    container_name: kibana
    depends_on:
      - elasticsearch  # Kibana se ejecuta después de Elasticsearch
    ports:
      - '5601:5601'  # Puerto de la interfaz de usuario de Kibana
```

## Explicación de la configuración

- **Elasticsearch**

  - Se utiliza la imagen oficial de Elasticsearch versión 8.10.2.
  - Se configura como un solo nodo (`discovery.type=single-node`).
  - Se deshabilita la seguridad (`xpack.security.enabled=false`) para facilitar el uso inicial.
  - Se expone el puerto `9200`, que permite acceder a la API REST de Elasticsearch.

- **Kibana**
  - Se usa la imagen oficial de Kibana versión 8.0.0.
  - Se establece una dependencia con Elasticsearch (`depends_on: - elasticsearch`), asegurando que Kibana se inicie después de que Elasticsearch esté disponible.
  - Se expone el puerto `5601`, que permite acceder a la interfaz de usuario de Kibana.

## Uso e implementación

### 1. Iniciar los servicios

Ejecuta el siguiente comando en la terminal dentro del directorio donde está el archivo `docker-compose.yml`:

```bash
docker-compose up -d
```

Este comando iniciará los contenedores en segundo plano (`-d` significa "detached mode").

### 2. Verificar el estado de los contenedores

Para asegurarse de que los servicios están corriendo correctamente, ejecuta:

```bash
docker ps
```

Deberías ver los contenedores `elasticsearch` y `kibana` en ejecución.

### 3. Acceder a los servicios

- **Elasticsearch**: Accede a `http://localhost:9200` para verificar si el servicio está en funcionamiento. Puedes probarlo con:

  ```bash
  curl -X GET "http://localhost:9200"
  ```

  Si está funcionando correctamente, devolverá información del nodo.

- **Kibana**: Abre `http://localhost:5601` en un navegador para acceder a la interfaz de usuario de Kibana.

## Conclusión

Esta configuración de Docker Compose permite desplegar Elasticsearch y Kibana de manera sencilla y rápida. Elasticsearch proporciona almacenamiento, indexación y búsqueda de datos, mientras que Kibana facilita su visualización y análisis. Juntos, forman una solución poderosa para el manejo de datos en tiempo real.
