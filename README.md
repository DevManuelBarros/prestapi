#   Prestapi.

## Descripción
Prestapi esa pequeña aplicación para acceder a la API de PrestaShop. Se realizo con el fin de que sea un poco más robusta de lo que ya existe. No solamente cumple con las funciones comunes sino que realiza algunas tareas más para más facilitarlo. Conceptualmente se divide en:


### Generales (Controles basicos )

#### Iniciar Prestapi
```python
#importamos la libreria
from PrestaShopWebservice import Prestapi

objeto = Prestapi(host='localhost:8080', protocol='https', key='key_from_prestashop')
```


### GET (Recuperar). search()

Aquí veremos la forma rapida de obtener resultado. Primero obtendremos sin filtros los 

```python
result = objeto.search(resource='manufacturers') # devuelve un objeto json
#resulta = objeto.search(resource='manufacturers', type_json=False) #Esta linea devolvería XML 
print(result.text)
```

Resultado
--

```python
{"manufacturers":[{"id":1,"active":"1","link_rewrite":"studio-design","name":"Studio Design","date_add":"2020-03-17 20:06:59","date_upd":"2020-03-17 20:06:59","description":"<p><span style=\"font-size:10pt;font-style:normal;\">Studio Design offers a range of items from ready-to-wear collections to contemporary objects. The brand has been presenting new ideas and trends since its creation in 2012.<\/span><\/p>","short_description":"","meta_title":"","meta_description":"","meta_keywords":"","associations":{"addresses":[{"id":"4"}]}},{"id":2,"active":"1","link_rewrite":"graphic-corner","name":"Graphic Corner","date_add":"2020-03-17 20:06:59","date_upd":"2020-03-17 20:06:59","description":"<p><span style=\"font-size:10pt;font-style:normal;\">Since 2010, Graphic Corner offers a large choice of quality posters, available on paper and many other formats. <\/span><\/p>","short_description":"","meta_title":"","meta_description":"","meta_keywords":""}]}
```

Filtrando campos.
--


```python
result = objeto.search(resource='manufacturers',display='id,name')
#Recordar que si pasamos con argumento type_json=False, devolvera un xml
print(result.text)
```

Resultado
--
```python
{"manufacturers":[
    {"id":1,"name":"Studio Design"},
    {"id":2,"name":"Graphic Corner"}
    ]}
```

Opción 2 (Filtro en devolución de campos)
===

```python
result = objeto.search(resource='countries', id_field='id',id_value='10')
print(result.text)
```

Resultado
--

```python
{"countries":[{
    "id":10,
    "id_zone":"1",
    "id_currency":"0",
    "call_prefix":"39",
    "iso_code":"IT",
    "active":"0",
    "contains_states":"1",
    "need_identification_number":"0",
    "need_zip_code":"1",
    "zip_code_format":"NNNNN",
    "display_tax_label":"1",
    "name":"Italy"}
    ]}
```




```python
result = objeto.search(resource='countries', id_field='id',id_value='10',display='id,name')
#Recordar que si pasamos con argumento type_json=False, devolvera un xml
print(result.text)
```

Resultado
--

```python
{"countries":[{"id":10,"name":"Italy"}]}
```


A
===

```python
result = objeto.search(resource='countries', id_field='id',id_value='[10|15|20]', display='id,name,active')
print(result.text)
```

Resultado
--

```python
{"countries":[{
    "id":10,"active":"0","name":"Italy"},
    {"id":15,"active":"0","name":"Portugal"},
    {"id":20,"active":"0","name":"Denmark"}
    ]}
```

B
===

```python
result = objeto.search(resource='countries', id_field='id',id_value='[10,25]', display='id,name,active')
print(result.text)
```

Resultado
--

```python
{"countries":[{
    "id":10,"active":"0","name":"Italy"},
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
```


### DELETE (Borrar)

El borrado de registros quiza es lo más sencillo de realizar. Simplemente tenemos que entidad queremos trabajar y el id del registro a eliminar. 

```python
result = objeto.delete(resource='addresses', id=11)
if result[0] == False:
    print("la petición a fallado. El mensaje: {}".format(result[1]))
else:
    print("La petición ha sido exitosa")
```

Resultado
--
Si nos da un error el resultado sería algo como lo siguiente

```
ERROR!... 
 This call to PrestaShop Web Services failed and returned an HTTP status of 404. 
 That means: Not Found. 
 Details: Recurso no encontrado. Se utiliza cuando el servidor web no encuentra la página o recurso solicitado..
```



### ADD (Agregar)


### PUT (Actualizar)


