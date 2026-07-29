# API Changelog

Este archivo documenta cambios y el estado actual de la API (endpoints y esquemas OpenAPI).

Formato por entrada:

- Fecha: YYYY-MM-DD
- Autor: autor
- Versión: (opcional)
- Endpoint(s) afectados: lista
- Descripción corta: resumen
- Detalles: parámetros, cuerpo, respuesta, notas de implementación

## [Unreleased] - 2026-07-29 Jessica Catalán

### Added
- Implementado endpoint `POST /posts` para la creación de publicaciones.
- Asociación de múltiples tags a un post mediante `tag_slugs`.
- Validación de existencia del autor utilizando `get_object_or_404`.
- Implementado endpoint `GET /posts/{post_id}` para obtener el detalle de una publicación.
- Incluido listado de comentarios asociados a la publicación.
- Incluida información del autor y tags en la respuesta del detalle.

### Changed
- Incremento automático del contador de visualizaciones (`view_count`) al consultar el detalle de un post.
- Optimizada la consulta de tags utilizando un único `filter(slug__in=...)` en lugar de múltiples consultas.
- Mejorada la serialización de autores, tags y comentarios para mantener una respuesta consistente.

### Fixed
- Verificada la correcta relación Many-to-Many entre `Post` y `Tag`.