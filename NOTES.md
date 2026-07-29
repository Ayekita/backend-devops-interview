# NOTES

## Qué hice y por qué

### 1. Optimización de rendimiento de los endpoints

Identifiqué que los listados de publicaciones presentaban un problema de consultas N+1 al cargar autores y etiquetas. Para solucionarlo incorporé `select_related()` y `prefetch_related()`, además de implementar paginación para evitar cargar decenas de miles de registros en una sola petición.

Con estos cambios se redujo significativamente el número de consultas a la base de datos y mejoró el tiempo de respuesta bajo carga.

### 2. Optimización de la base de datos

Analicé el plan de ejecución de PostgreSQL mediante `EXPLAIN ANALYZE` y detecté que el listado principal realizaba un recorrido secuencial sobre la tabla de publicaciones. Para optimizarlo agregué un índice compuesto sobre los campos `is_published` y `created_at`, permitiendo que PostgreSQL utilizara un índice para resolver la consulta de forma más eficiente.

### 3. Incorporación de pruebas automatizadas

Agregué y actualicé pruebas para validar el funcionamiento de los principales endpoints de la API, incluyendo:

- Listado de publicaciones.
- Búsqueda de publicaciones.
- Filtrado por etiquetas.
- Creación de publicaciones.
- Creación de comentarios.
- Consulta de usuarios.

Esto permitió validar que los cambios realizados no introdujeran regresiones y mejorar la confiabilidad del proyecto.

---

## Qué dejé fuera deliberadamente

Decidí no implementar autenticación, autorización, caché o procesamiento asíncrono, ya que consideré que escapaban al alcance del desafío y preferí dedicar el tiempo a mejorar el rendimiento, la calidad del código y la cobertura de pruebas.

Tampoco agregué pruebas para los comandos de administración (como el comando de carga de datos), ya que son herramientas de soporte y no forman parte del comportamiento principal de la aplicación.

---

## Qué haría si tuviera un día más

Si dispusiera de un día adicional, me enfocaría en:

- Incorporar paginación basada en cursores (cursor pagination) para mejorar el rendimiento con grandes volúmenes de datos.
- Agregar una capa de caché para los endpoints de lectura más utilizados.
- Aumentar la cobertura de pruebas incluyendo casos límite y pruebas de rendimiento.
- Incorporar logging estructurado y métricas básicas para facilitar el monitoreo y diagnóstico de la aplicación.