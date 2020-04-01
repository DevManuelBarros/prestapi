#   Prestapi.

## Descripción
Prestapi esa pequeña aplicación para acceder a la API de PrestaShop. Se realizo con el fin de que sea un poco más robusta de lo que ya existe. No solamente cumple con las funciones comunes sino que realiza algunas tareas más para más facilitarlo. Conceptualmente se divide en:


### Generales (Controles basicos )

#### Iniciar Prestapi
~~~
#importamos la libreria
from PrestaShopWebservice import Prestapi

objeto = Prestapi(host='localhost:8080', protocol='https', key='key_from_prestashop')
~~~

#### Busquedas generales.

Opción 1
===
traeremos todos los resultados de una entidad en particular en este caso elegiremos 'manufacturers', que serían direcciones para lo mismo haremos lo siguiente:

~~~
objeto.set_params_get(resource='manufacturers',display_full=True)
objeto.define_json() # devolvera un elemento Json
#objeto.define_json(type_json=False)   #devolvera un elemento tipo Xml
result = tmp = objeto.executeRequest() #ejecutaremos la consulta.
~~~

Resultado
--

~~~
{"manufacturers":[{"id":1,"active":"1","link_rewrite":"studio-design","name":"Studio Design","date_add":"2020-03-17 20:06:59","date_upd":"2020-03-17 20:06:59","description":"<p><span style=\"font-size:10pt;font-style:normal;\">Studio Design offers a range of items from ready-to-wear collections to contemporary objects. The brand has been presenting new ideas and trends since its creation in 2012.<\/span><\/p>","short_description":"","meta_title":"","meta_description":"","meta_keywords":"","associations":{"addresses":[{"id":"4"}]}},{"id":2,"active":"1","link_rewrite":"graphic-corner","name":"Graphic Corner","date_add":"2020-03-17 20:06:59","date_upd":"2020-03-17 20:06:59","description":"<p><span style=\"font-size:10pt;font-style:normal;\">Since 2010, Graphic Corner offers a large choice of quality posters, available on paper and many other formats. <\/span><\/p>","short_description":"","meta_title":"","meta_description":"","meta_keywords":""}]}
~~~

### ADD (Agregar)

### GET (Recuperar)

### DELETE (Borrar)

### PUT (Actualizar)