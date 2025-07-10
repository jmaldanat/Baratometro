
# Manual: Cómo usar fixtures en Django para agregar posts

## ¿Qué es un fixture?
Un archivo con datos (JSON, XML, YAML) para llenar tablas de la base de datos automáticamente.

## ¿Por qué usarlo?
✅ Ahorras tiempo.  
✅ No necesitas meter datos a mano en el admin panel.  
✅ Útil para pruebas, demos o recuperar datos tras errores.

## Pasos rápidos para agregar posts usando fixtures

1️⃣ **Crear carpeta fixtures**
- En tu app `blog`, crea una carpeta llamada `fixtures`.

2️⃣ **Crear archivo JSON**
- Dentro de `blog/fixtures`, crea `posts.json`.

3️⃣ **Agregar datos JSON**
- Copia el contenido del archivo fuente (te lo da el curso o lo haces tú) y pégalo en `posts.json`.

4️⃣ **Cargar datos en la base**
- Corre en terminal:
  ```
  python3 manage.py loaddata posts
  ```
  Django buscará automáticamente `blog/fixtures/posts.json`.

5️⃣ **Ignorar fixtures en Git**
- En `.gitignore`, agrega:
  ```
  blog/fixtures/
  ```
  Así no subes esos datos al repositorio.

6️⃣ **Verificar en el admin panel**
- Levanta el servidor:
  ```
  python3 manage.py runserver
  ```
- Ve a tu navegador: `http://localhost:8000/admin`  
- Entra con tu superuser y revisa los posts en la sección **Posts**.

## Notas clave
⚠️ Las fechas (`created_on`) vienen del JSON, así que pueden ser anteriores a los posts que metiste manualmente.  
⚡ Si tu base se borra por error, puedes recargarla usando este método.

## Resumen final
Usa fixtures para:
- Poblaciones masivas de datos.
- Pruebas de funcionalidades (como paginación).
- Demos para colegas, clientes o entrevistas.
