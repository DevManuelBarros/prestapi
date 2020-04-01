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

Opción 1 (Sin Filtro)
===
traeremos todos los resultados de una entidad en particular en este caso elegiremos 'manufacturers' (resource='manufacturers'), que serían direcciones para lo mismo haremos lo siguiente:

~~~

objeto.set_params_get(resource='manufacturers',display_full=True)
objeto.define_json() # devolvera un elemento Json
#objeto.define_json(type_json=False)   #devolvera un elemento tipo Xml
result = tmp = objeto.executeRequest() #ejecutaremos la consulta.
print(result.text)
~~~

Resultado
--

~~~
{"manufacturers":[{"id":1,"active":"1","link_rewrite":"studio-design","name":"Studio Design","date_add":"2020-03-17 20:06:59","date_upd":"2020-03-17 20:06:59","description":"<p><span style=\"font-size:10pt;font-style:normal;\">Studio Design offers a range of items from ready-to-wear collections to contemporary objects. The brand has been presenting new ideas and trends since its creation in 2012.<\/span><\/p>","short_description":"","meta_title":"","meta_description":"","meta_keywords":"","associations":{"addresses":[{"id":"4"}]}},{"id":2,"active":"1","link_rewrite":"graphic-corner","name":"Graphic Corner","date_add":"2020-03-17 20:06:59","date_upd":"2020-03-17 20:06:59","description":"<p><span style=\"font-size:10pt;font-style:normal;\">Since 2010, Graphic Corner offers a large choice of quality posters, available on paper and many other formats. <\/span><\/p>","short_description":"","meta_title":"","meta_description":"","meta_keywords":""}]}
~~~

Opción 2 (Filtro en devolución de campos)

En este caso definiremos lo que traeremos pero nada más. Quitamos el argumento display_full=True de set.params.get() y agregamos la función display_params y enviamos un string con los campos separados por coma que queremos que nos devuelva.

===
~~~
objeto.set_params_get(resource='manufacturers')
objeto.display_params('id,name')
objeto.define_json() # devolvera un elemento Json
#objeto.define_json(type_json=False)   #devolvera un elemento tipo Xml
result = tmp = objeto.executeRequest() #ejecutaremos la consulta.
print(result.text)
~~~


Resultado
--

~~~
{"manufacturers":[{"id":1,"name":"Studio Design"},{"id":2,"name":"Graphic Corner"}]}
~~~
Mucho más claro y más afinada la busqueda.

 Lo anterior funciono bien, pero ahora queremos solo traer algunos campos. Para obtener solamente la información que nos importa.

Opción 3 (a.Filtro por valores)
===

Ahora lo que haremos será trabajar sobre una entidad más grande (countries) y comenzaremos a realizar algunos filtros más complejos.  
La entidad countries trae de por si registros por defecto y nos permitira demostrar como trabajar con estos registros.

Lo que haremos ahora sera primero traer un solo campo, filtraremos por el id de la entiedad, elegiremos el registro 10.

Para esto usaremos filter_params(id_field='el nombre del campo', id_value='valor que queremos obtener')
~~~
objeto.set_params_get(resource='countries')
objeto.filter_params(id_field='id',id_value='10') #Aqui esta el filtro
objeto.define_json() # devolvera un elemento Json
#objeto.define_json(type_json=False)   #devolvera un elemento tipo Xml
result = tmp = objeto.executeRequest() #ejecutaremos la consulta.
print(result.text)
~~~

El resultado sería algo como lo siguiente:
--
~~~
{"countries":[
    {"id":10,"id_zone":"1",
    "id_currency":"0",
    "call_prefix":"39",
    "iso_code":"IT","active":"0",
    "contains_states":"1",
    "need_identification_number":"0",
    "need_zip_code":"1",
    "zip_code_format":"NNNNN",
    "display_tax_label":"1",
    "name":"Italy"}
    ]}
~~~

Opción 3. (b.Filtro trayendo campos) 
--

Pero quiza solo necesitemos traer algunos campos nada más, por ejemplo: 'id', 'name' y 'active'. Podríamos hacerlo de la siguiente manera:

~~~
objeto.set_params_get(resource='countries')
objeto.filter_params(id_field='id',id_value='10', display='id,name,active')
objeto.define_json() # devolvera un elemento Json
#objeto.define_json(type_json=False)   #devolvera un elemento tipo Xml
result = tmp = objeto.executeRequest() #ejecutaremos la consulta.
print(result.text)
~~~

Resultado
--
~~~
{"countries":[{"id":10,"active":"0","name":"Italy"}]}
~~~


Opción 3. (c.Filtro con rangos) 
--

Perfecto, pero si queres más campos que estos solos, queremos filtrar el campo 10, 15 y 20. Haríamos lo siguiente:

~~~
objeto.set_params_get(resource='countries')
objeto.filter_params(id_field='id',id_value='[10|15|20]', display='id,name,active')
objeto.define_json() # devolvera un elemento Json
#objeto.define_json(type_json=False)   #devolvera un elemento tipo Xml
result = tmp = objeto.executeRequest() #ejecutaremos la consulta.
print(result.text)
~~~

Lo unico que se modifico fue el id_value =[] los valores separados por el caracter "|" nos permite pasar una lista de valores como argumentos.


Resultado
--
~~~
{"countries":[
    {"id":10,"active":"0","name":"Italy"},
    {"id":15,"active":"0","name":"Portugal"},
    {"id":20,"active":"0","name":"Denmark"}
    ]
}
~~~

Otra cosa interesante serían rangos, quisieramos del id = 10 al 25. Hariamos lo siguiente:

~~~
objeto.set_params_get(resource='countries')
objeto.filter_params(id_field='id',id_value='[10,25]', display='id,name,active')
objeto.define_json() # devolvera un elemento Json
#objeto.define_json(type_json=False)   #devolvera un elemento tipo Xml
result = tmp = objeto.executeRequest() #ejecutaremos la consulta.
print(result.text)
~~~

Resultado
--
~~~
{"countries":[
    {"id":10,"active":"0","name":"Italy"},
    {"id":11,"active":"0","name":"Japan"},
    {"id":12,"active":"0","name":"Luxemburg"},
    {"id":13,"active":"0","name":"Netherlands"},
    {"id":14,"active":"0","name":"Poland"},
    {"id":15,"active":"0","name":"Portugal"},
    {"id":16,"active":"0","name":"Czech Republic"},
    {"id":17,"active":"0","name":"United Kingdom"},
    {"id":18,"active":"0","name":"Sweden"},
    {"id":19,"active":"0","name":"Switzerland"},
    {"id":20,"active":"0","name":"Denmark"},
    {"id":21,"active":"1","name":"United States"},
    {"id":22,"active":"0","name":"HongKong"},
    {"id":23,"active":"0","name":"Norway"},
    {"id":24,"active":"0","name":"Australia"},
    {"id":25,"active":"0","name":"Singapore"}
    ]}
~~~




### ADD (Agregar)

### GET (Recuperar)

### DELETE (Borrar)

### PUT (Actualizar)