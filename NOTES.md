# NOTES

## Qué hice y por qué

### 1. Optimización de rendimiento de los endpoints

Identifiqué un problema de consultas N+1 al obtener publicaciones junto con sus autores y etiquetas. Para solucionarlo incorporé `select_related()` y `prefetch_related()`, además de implementar paginación para evitar cargar grandes volúmenes de registros en una sola petición.

Estas mejoras reducen la cantidad de consultas ejecutadas por el ORM y hacen que los endpoints sean más eficientes y escalables.

### 2. Optimización de la base de datos

Analicé el plan de ejecución de PostgreSQL utilizando `EXPLAIN ANALYZE` y detecté que el listado principal realizaba un recorrido secuencial sobre la tabla `post`. Para optimizar esta consulta agregué un índice compuesto sobre los campos `is_published` y `created_at`, permitiendo que PostgreSQL aproveche el índice durante la búsqueda y ordenamiento.

### 3. Implementación de nuevos endpoints

Se implementaron los endpoints necesarios para completar la funcionalidad del servicio:

- Creación de publicaciones (`POST /posts`).
- Obtención del detalle de una publicación (`GET /posts/{post_id}`).
- Asociación de etiquetas mediante `tag_slugs`.
- Incremento automático del contador de visualizaciones (`view_count`) al consultar el detalle de una publicación.

### 4. Incorporación de pruebas automatizadas

Agregué y actualicé pruebas para validar el funcionamiento de los principales endpoints de la API, incluyendo:

- Listado de publicaciones.
- Búsqueda de publicaciones.
- Filtrado por etiquetas.
- Creación de publicaciones.
- Creación de comentarios.
- Consulta de usuarios.

Esto permitió validar que los cambios realizados no introdujeran regresiones y mejorar la confiabilidad del proyecto.

## Mejoras de Developer Experience y Production Readiness

Con el objetivo de facilitar la ejecución del proyecto y dejarlo preparado para un entorno más cercano a producción, se incorporaron las siguientes mejoras:

- Externalización de la configuración mediante variables de entorno (`.env.example`), evitando valores sensibles dentro del código fuente.
- Incorporación de Docker y Docker Compose para levantar el entorno completo (aplicación y PostgreSQL) de forma reproducible.
- Configuración de Gunicorn como servidor WSGI para la ejecución de la aplicación dentro del contenedor.
- Automatización de la ejecución de migraciones al iniciar la aplicación mediante un `entrypoint.sh`.
- Persistencia de la base de datos utilizando un volumen de Docker.
- Configuración de un `healthcheck` para PostgreSQL, asegurando que la aplicación espere a que la base de datos esté disponible antes de iniciar.

Estas mejoras permiten que cualquier persona pueda levantar el proyecto con una configuración mínima y acercan la solución a un entorno de despliegue real.

---

## Qué dejé fuera deliberadamente

Decidí no implementar autenticación, autorización, caché o procesamiento asíncrono, ya que consideré que escapaban al alcance del desafío y preferí dedicar el tiempo a mejorar el rendimiento, la calidad del código y la cobertura de pruebas.

Tampoco agregué pruebas para los comandos de administración (como el comando de carga de datos), ya que son herramientas de soporte y no forman parte del comportamiento principal de la aplicación.

---

## Qué haría si tuviera un día más

Si dispusiera de un día adicional, me enfocaría en:

- Implementar autenticación basada en JWT para proteger los endpoints de escritura, utilizando el sistema de autenticación de Django o una solución compatible con el modelo actual.
- Configurar un pipeline de CI para ejecutar automáticamente Ruff, pruebas y cobertura en cada cambio.
- Incorporar una capa de caché para los endpoints de lectura más utilizados.
- Ampliar la cobertura de pruebas con casos límite y pruebas de rendimiento.
- Agregar logging estructurado y métricas para facilitar el monitoreo de la aplicación.

---

## Optimización del Seed

Se realizaron mejoras al proceso de generación de datos para reducir el tiempo de ejecución y el consumo de recursos, manteniendo una implementación simple basada en el ORM de Django.

### Mejoras implementadas

- Se aumentó el tamaño de los lotes (`bulk_create`) de **1.000** a **5.000** registros para reducir la cantidad de operaciones de inserción en la base de datos.
- Se reutilizaron datos generados con **Faker** mediante pools de títulos, cuerpos de publicaciones y comentarios, evitando generar contenido nuevo para cada registro.
- Se optimizó la obtención de identificadores utilizando `values_list()`, reduciendo el uso de memoria al evitar cargar objetos completos del ORM.
- Se agruparon las inserciones masivas dentro de transacciones (`transaction.atomic()`), disminuyendo el costo asociado a múltiples confirmaciones de escritura.
- Se redujo el número de consultas innecesarias durante el proceso de generación de datos.

Estas optimizaciones permiten generar grandes volúmenes de información (100.000 publicaciones y 500.000 comentarios) de forma considerablemente más eficiente, sin sacrificar la legibilidad ni la mantenibilidad del código.

---

## Uso de IA

Utilicé herramientas de IA como apoyo para analizar alternativas, revisar código y acelerar algunas tareas de implementación y documentación.

Todas las decisiones técnicas, optimizaciones y cambios incorporados fueron revisados, adaptados y validados manualmente antes de formar parte de la solución final.

https://chatgpt.com/share/6a6ab2bb-41b0-83e9-902d-fddb86ad8e1a
