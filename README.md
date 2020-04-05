#   Prestapi.

## Descripción
Prestapi esa pequeña aplicación para acceder a la API de PrestaShop. Se realizo con el fin de que sea un poco más robusta de lo que ya existe. No solamente cumple con las funciones comunes sino que realiza algunas tareas más para facilitar la interacción. Conceptualmente se divide en:


# Generales (Controles basicos )
* GET    --> search()
* DELETE --> delete()
* PUT    --> update()
* ADD    --> add()

# Iniciar Prestapi

```python
#importamos la libreria
from PrestaShopWebservice import Prestapi

objeto = Prestapi(host='localhost:8080', protocol='https', key='key_from_prestashop')
```


# SEARCH (Recuperar)

Aquí veremos la forma rapida de obtener resultado. Primero obtendremos sin filtros los 

```python
result = objeto.search(resource='manufacturers') # devuelve un objeto json
#resulta = objeto.search(resource='manufacturers', type_json=False) #Esta linea devolvería XML 
print(result.text)
```

**Resultado**


```json
{"manufacturers":[
    {
    "id":1,
    "active":"1",
    "link_rewrite":"studio-design",
    "name":"Studio Design",
    "date_add":"2020-03-17 20:06:59",
    "date_upd":"2020-03-17 20:06:59",
    "description":"<p><span style=\"font-size:10pt;font-style:normal;\">Studio Design offers a range of items from ready-to-wear collections to contemporary objects. The brand has been presenting new ideas and trends since its creation in 2012.<\/span><\/p>","short_description":"",
    "meta_title":"",
    "meta_description":"",
    "meta_keywords":"",
    "associations":{"addresses":[{"id":"4"}]}
    },
    {
    "id":2,"active":"1",
    "link_rewrite":"graphic-corner",
    "name":"Graphic Corner",
    "date_add":"2020-03-17 20:06:59",
    "date_upd":"2020-03-17 20:06:59",
    "description":"<p><span style=\"font-size:10pt;font-style:normal;\">Since 2010, Graphic Corner offers a large choice of quality posters, available on paper and many other formats. <\/span><\/p>","short_description":"",
    "meta_title":"",
    "meta_description":"",
    "meta_keywords":""
    }
    ]}
```

## Filtrando campos.



```python
result = objeto.search(resource='manufacturers',display='id,name')
#Recordar que si pasamos con argumento type_json=False, devolvera un xml
print(result.text)
```

**Resultado**

```json
{"manufacturers":[
    {"id":1,"name":"Studio Design"},
    {"id":2,"name":"Graphic Corner"}
    ]}
```


```python
result = objeto.search(resource='countries', id_field='id',id_value='10')
print(result.text)
```

**Resultado**


```json
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


## Filtro en devolución de campos

Aqui haremos lo que en SQL es normalmente el SELECT de los campos.


```python
result = objeto.search(resource='countries', id_field='id',id_value='10',display='id,name')
#Recordar que si pasamos con argumento type_json=False, devolvera un xml
print(result.text)
```

**Resultado**

```json
{"countries":[{"id":10,"name":"Italy"}]}
```


A
===

```python
result = objeto.search(resource='countries', id_field='id',id_value='[10|15|20]', display='id,name,active')
print(result.text)
```

**Resultado**


```json
{"countries":[{
    "id":10,"active":"0","name":"Italy"},
    {"id":15,"active":"0","name":"Portugal"},
    {"id":20,"active":"0","name":"Denmark"}
    ]}
```

## B

```python
result = objeto.search(resource='countries', id_field='id',id_value='[10,25]', display='id,name,active')
print(result.text)
```

**Resultado**


```json
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


# DELETE (Borrar)

El borrado de registros quiza es lo más sencillo de realizar. Simplemente tenemos que entidad queremos trabajar y el id del registro a eliminar. 

```python
result = objeto.delete(resource='addresses', id=11)
if result[0] == False:
    print("La petición a fallado. El mensaje: {}".format(result[1]))
else:
    print("La petición ha sido exitosa")
```

**Resultado**

Si nos da un error el resultado sería algo como lo siguiente

```
La petición a fallado. El mensaje: ERROR!... 
 This call to PrestaShop Web Services failed and returned an HTTP status of 404. 
 That means: Not Found. 
 Details: Recurso no encontrado. Se utiliza cuando el servidor web no encuentra la página o recurso solicitado..
```



# ADD (Agregar)

Es importante primero saber que para poder grabar datos es necesario recuperar la estructura. Prestapi, permite dos forma de realizarlo, la primera un poco más manual y la otra una forma un poquito más robusta. Primero veamos la forma más simple y sencilla de realizarlo que simplemente implicaría recuperar la escructura requerida en formato json, llenarla y enviarla al servidor para grabarla. Lo primero que haremos será traer la estructura a través de ***get_struct()***.

tmpResult = objeto.get_struct('addresses')


```python
tmpResult = objeto.get_struct('addresses')
print(tmpResult)
```

La función get_struct permite definir tres parametros:
* resource = Entidad con la que queremos trabajar.
* schema = Por default se carga en 'blank' con lo cual trae la estructura. Y en el caso de 'synopsis' devolvera el formato especifico de la entidad a rellenar con datos como si es obligatorio y el tipo de formato que soporta.
* type_json = Por defecto es True y es el tipo de formato que devolvera. Si es true sera en json y si el false en XML.


**Resultado**

```json
{"address":
        {"id":"",
        "id_customer":"",
        "id_manufacturer":"",
        "id_supplier":"",
        "id_warehouse":"",
        "id_country":"",
        "id_state":"",
        "alias":"",
        "company":"",
        "lastname":"",
        "firstname":"",
        "vat_number":"",
        "address1":"",
        "address2":"",
        "postcode":"",
        "city":"",
        "other":"",
        "phone":"",
        "phone_mobile":"",
        "dni":"",
        "deleted":"",
        "date_add":"",
        "date_upd":""
        }
    }
```

Recuperamos el listado con los requerimientos de cada campo. Para esto seteamos ***type_json=False*** para que devuelva un xml y ***schema='synopsis'***.

```python
tmpResult = objeto.get_struct('addresses', schema='synopsis', type_json=False)
print(tmpResult)
```

**Resultado**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
<address>
        <id_customer format="isNullOrUnsignedId"></id_customer>
        <id_manufacturer format="isNullOrUnsignedId"></id_manufacturer>
        <id_supplier format="isNullOrUnsignedId"></id_supplier>
        <id_warehouse format="isNullOrUnsignedId"></id_warehouse>
        <id_country required="true" format="isUnsignedId"></id_country>
        <id_state format="isNullOrUnsignedId"></id_state>
        <alias required="true" maxSize="32" format="isGenericName"></alias>
        <company maxSize="255" format="isGenericName"></company>
        <lastname required="true" maxSize="255" format="isName"></lastname>
        <firstname required="true" maxSize="255" format="isName"></firstname>
        <vat_number format="isGenericName"></vat_number>
        <address1 required="true" maxSize="128" format="isAddress"></address1>
        <address2 maxSize="128" format="isAddress"></address2>
        <postcode maxSize="12" format="isPostCode"></postcode>
        <city required="true" maxSize="64" format="isCityName"></city>
        <other maxSize="300" format="isMessage"></other>
        <phone maxSize="32" format="isPhoneNumber"></phone>
        <phone_mobile maxSize="32" format="isPhoneNumber"></phone_mobile>
        <dni maxSize="16" format="isDniLite"></dni>
        <deleted format="isBool"></deleted>
        <date_add format="isDate"></date_add>
        <date_upd format="isDate"></date_upd>
</address>
</prestashop>
```

Con esto podemos ver cuales son los campos requeridos y algunos requerimientos extras, por ejemplo el largo maximo de la cadena y el tipo de formato requerido, en el caso de ***id_country*** es un numero entero sin signo.

* alias : MaxSize = 32
* lastname : MaxSize = 255
* firstname : MaxSize  = 255
* address1 : MaxSize = 128
* postcode : MaxSize = 12
* city : MaxSize = 64
* id_country : Format : IsUnsignedId

Completamos los datos:

```python
tmpResult = objeto.get_struct('addresses')

tmpResult['address']['alias']  = 'Dirección1'
tmpResult['address']['lastname'] = 'Unapellido'
tmpResult['address']['firstname'] = 'Unnombre'
tmpResult['address']['address1'] = 'Una dirección'
tmpResult['address']['postcode'] = '1234567'
tmpResult['address']['city'] = 'Buenos Aires'
tmpResult['address']['id_country'] = 1 

print(tmpResult)
```


**Resultado**

```json
        {'address': 
                {'id': '',
                'id_customer': '', 
                'id_manufacturer': '', 
                'id_supplier': '', 
                'id_warehouse': '', 
                'id_country': 1, 
                'id_state': '', 
                'alias': 'Dirección1', 
                'company': '', 
                'lastname': 'Unapellido', 
                'firstname': 'Unnombre', 
                'vat_number': '', 
                'address1': 'Una dirección', 
                'address2': '', 
                'postcode': '1234567', 
                'city': 'Buenos Aires', 
                'other': '', 'phone': '', 
                'phone_mobile': '', 
                'dni': '', 
                'deleted': '', 
                'date_add': '', 
                'date_upd': ''
                }
            }

```


# PUT (Actualizar)


