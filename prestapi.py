#Imports generales
import requests
import os.path
import json
import dicttoxml

from xml.etree import ElementTree

#Imports particulares
from const_rel import relations

class Prestapi:
    """
    def __init__: Inicializa la clase
    ---\n
    @host : (str) cadena que contiene el host adonde debemos acceder.\n
    @key :  (str) cadena con la clave que nos entrego PrestaShop\n
    @protocol : (str) define el procolo por medio del cual se va a acceder, https o http, http es por defecto.
    @debug : (bool) Informa si debug esta activo, por defecto es True \n
    """
    def __init__(self, host, key, protocol="http", debug=True):
        self.host = host                #El host donde esta alojado la API
        self.key = key                  #key que entrega PrestaShop cuando la generamos
        self.debug = debug              #Si esta en modo debug o no
        self.version = 'unknown'        #Versión de la api de prestashop
        #configuracion por defector de la cabecera de las peticiones realizadas
        self.default_headers = {
                                'Io-Format' : '',
                                'Output-Format' : '',
                                'User-Agent': 'Prestapi.py by Manuel Barros',
                              }
        #default settings son los parametros que casi siempre se necesitaran
        self.default_params = {'resource':'',
                                'id':'',
                                'schema' : ''}
        #Otros parametros que podemos utilizar para para obtener datos, etc.
        #self.other_params = {
        #                    'filter' : '',
        #                    'sort' : '',
        #                    'limit' : '',
        #                    'id_shop' : '',
        #                    'id_group_shop' : ''
        #                    }
        self.int_params = {}
        self.line_for_format = ""
        self.dict_format = {
                            'isNullOrUnsigned' : self.fun,
                            'isUnsignedId'     : self.fun,
                            'isGenericName'    : self.fun,
                            'isName'           : self.fun,
                            'isAddress'        : self.fun,
                            'isPostCode'       : self.fun,
                            'isCityName'       : self.fun,
                            'isMessage'        : self.fun,
                            'isPhoneNumber'    : self.fun,
                            'isDniLite'        : self.fun,
                            'isDate'           : self.fun,
                            'isBool'           : self.fun,
                          }
        self.psCompatibleVersionsMin = '1.7.0.0'            #La minima versión comprobada que funciona con esta APP
        self.psCompatibleVersionsMax = '1.7.99.99'          #La maxima versión comprobada que funciona con esta APP
        self.protocol = protocol + "://"                    #creamos la cadena para el protocolo
        self.dir_cache = "cache/"                           #configuracion de la carpeta que hara de cache
        

    def limit_params(self, number, starindex=0):
        self.int_params['limit'] = "{},{}".format(starindex,number)

    def filter_params(self, id_field, id_value, display=False):
        #{'filter[id]':'[10,250]','display':'[id,name]'}
        self.int_params["filter[{}]".format(id_field)] = id_value
        self.display_params(display=display)

    def display_params(self, display=False):
        if display != False:
            self.int_params['display'] = '[' + display + ']'
        else:
            self.int_params['display'] = 'full'



    def search(self, resource, id_field=False,id_value=False, display=False, type_json=True):
        self.set_params_get(resource=resource)
        if id_field!= False and id_value!=False:
            self.filter_params(id_field=id_field, id_value=id_value,display=display)
            self.set_params_get(resource=resource)
        else:
            self.set_params_get(resource=resource)
            self.display_params(display=display)
        self.define_json(type_json=type_json)
        result = self.executeRequest()
        return result

    """
    def checkStatusCode: Control del estado de las peticiones.
    ---\n
    @status_code: (int) Numero de respuesta de la peticion realizada.\n
    """
    def checkStatusCode(self, status_code):
        error_label = 'ERROR!... \n This call to PrestaShop Web Services failed and returned an HTTP status of {}. \n That means: {}. \n Details: {}.'
        msg_label = 'OK!... \n This call to Prestashop Web Services returned an HTTO status of {}. \n That means: {}. \n Details: {}.'
        case = {200 : msg_label.format(status_code, 'Ok', 'Respuesta estándar para peticiones correctas.'),
                201: msg_label.format(status_code, 'Created', 'La petición ha sido completada y ha resultado en la creación de un nuevo recurso.'),
                202: msg_label.format(status_code, 'Accepted', 'La petición ha sido aceptada para procesamiento, pero este no ha sido completado. La petición eventualmente pudiere no ser satisfecha, ya que podría ser no permitida o prohibida cuando el procesamiento tenga lugar.'),
                203: msg_label.format(status_code,'Non-Authoritative Information','La petición se ha completado con éxito, pero su contenido no se ha obtenido de la fuente originalmente solicitada sino de otro servidor.'),
                401: error_label.format(status_code,'Unauthorized','Similar al 403 Forbidden, pero específicamente para su uso cuando la autentificación es posible pero ha fallado o aún no ha sido provista'),
                404: error_label.format(status_code, 'Not Found', 'Recurso no encontrado. Se utiliza cuando el servidor web no encuentra la página o recurso solicitado.'),
                405: error_label.format(status_code, 'Method Not Allowed', 'Una petición fue hecha a una URI utilizando un método de solicitud no soportado por dicha URI; por ejemplo, cuando se utiliza GET en un formulario que requiere que los datos sean presentados vía POST, o utilizando PUT en un recurso de solo lectura.'),
                406: error_label.format(status_code, 'Not Acceptable', 'El servidor no es capaz de devolver los datos en ninguno de los formatos aceptados por el cliente, indicados por éste en la cabecera "Accept" de la petición.'),
                500: error_label.format(status_code, 'Internal Server Error', 'Es un código comúnmente emitido por aplicaciones empotradas en servidores web, mismas que generan contenido dinámicamente, por ejemplo aplicaciones montadas en IIS o Tomcat, cuando se encuentran con situaciones de error ajenas a la naturaleza del servidor web.'),
                }
        if status_code in case:
            return case.get(status_code)
        else:
            return 'Unknown!... \n This call to PrestaShop Web Services returned an unexpected HTTP status of {}. \n Details: {}'.format(status_code, 'Desconocido totalmente el comando.')

    """
    def change_params: Agrega o cambia totalmente los parametros
    ---\n
    @params : (dict) Los parametros a agregar o colocar dentro del diccionario por default\n
    @add : (bool) si estan en True, como por defecto, agrega al diccionario o en caso contrario modifica totalmente la cabecera\n
    """
    def change_params(self, params={}, add=True):
        if add == True:                         #Comprobamos si hay que agregar o crear nuevos parametros
            for k, v in params.items():         #recorremos los parametros pasados como args.
                self.default_params[k] = v      #los agregamos a los que ya existen
        else:
            self.default_params = params        #simplemente reemplazamos los parametros
        return self.default_params
    
    """
    def change_headers: Agrega o cambia totalmente los parametros
    ---\n
    @headers : (dict) Los parametros a agregar o colocar dentro del diccionario por default\n
    @add : (bool) si estan en True, como por defecto, agrega al diccionario o en caso contrario modifica totalmente la cabecera\n
    """
    def change_headers(self, headers={}, add=True):
        if add == True:                             #Comprobamos si hay que agregar o crear nuevos parametros
            for k, v in headers.items():            #recorremos los parametros pasados como args.
                self.default_headers[k] = v         #los agregamos a los que ya existen
        else:
            self.default_headers = headers          #simplemente reemplazamos los parametros
        return self.default_headers
    
    """
    def executeRequest: Metodo interno para terminar de ejecutar la peticion con requests
    ---\n
    @metod = (str) Aqui sugerimos que metodo se realizara. GET, POST, etc.
    @url   = (str) La url por defecto estara en False, pero se puede pasar y no se construye.
    """
    def executeRequest(self,  method='GET', data=False, url=False):
        if url == False:
            url_full = self.make_full_url()
        else:
            url_full = url
        session = requests.Session()
        req = requests.Request(method, 
                               url_full,
                               params=self.int_params,
                               headers=self.default_headers,
                               data=data,
                               auth=(self.key,'')
                               )
        response = session.send(req.prepare(), verify=True)
        self.default_params = {'resource':'',
                                'id':'',
                                'schema' : ''}
        self.clear_headers()
        self.int_params = {}
        return response

    """
    def set_params_get: para setear los parametros.
    \n
    @resource : (str)
    @id : (str)
    @schema : (str)
    """
    def set_params_get(self, resource=False, id=False, schema=False,display_full=False):
        #Todos los args son opcionales, si no se coloca nada borrara los valores.j
        #en caso de que se envien valores se modificaran.
        self.default_params['resource'] = resource if resource != False else ''
        self.default_params['id'] = id if id != False else ''
        self.default_params['schema'] = schema if schema != False else ''
        if display_full == True:
            self.display_params()


    """
    def make_param:
    \n
   
    def make_param(self):
        other_params = ""
        for k, v in self.other_params.items():
            if v != "":
                other_params += k+"="+v+"&"
        other_params = other_params.strip()
        return other_params[:-1]
    """

    """
    def make_full_url:
    \n
    """
    def make_full_url(self):
        #Controlamos que la parte 
        url = self.protocol + self.host if not(self.protocol in self.host) else self.host
        #agregamos /api/ al host.
        url = url + "/api/" if url[-1]!="/" else url + "api/"
        #agregamos el resource que se esta intentando acceder
        url = url  + self.default_params['resource'] if self.default_params['resource'] != '' else url
        url = url + "/" +  self.default_params['id'] if self.default_params['id'] != '' else url
        url = url + "?schema=" + self.default_params['schema'] if self.default_params['schema'] != '' else url 
        """
        new_param = self.make_param()
        if "?" in url:
            url = url + "&" + new_param if new_param != '' else url
        else:
            url = url + "?" + new_param if new_param != '' else url 
        """
        return str(url)
        

    """
    def define_json: 
    Esto definira las valores de la cabecera sobre la entrada y salida de datos, por defecto
    se realizara con JSON, es decir si no se pasan argumentos.
    \n
    @type_json : (bool) si es True el tipo de archivo de salida y entrada sera Json, 
    caso contrario sera XML
    """
    def define_json(self, type_json=True):
        if type_json==True:
            self.default_headers['Output-Format'] = 'JSON'
            self.default_headers['Io-Format'] = 'JSON'
            self.default_headers['Content-Type'] = 'text/json'
        else:
            self.default_headers['Output-Format'] = 'XML'
            self.default_headers['Io-Format'] = 'XML'
            self.default_headers['Content-Type'] = 'text/xml'



    #
    #-------------- ADD ----------------
    #Sector para el agregado de valores.
    #-----------------------------------


    def g_id_name(self, resource, name):
        result = {}
        if name == 'None':
            return  {'id' : None}
        else:
            self.define_json()
            self.set_params_get(resource=resource)
            self.display_params(display=name)
            result = self.executeRequest()
        return result.json()

    """
    def get_rules_dict:  convertiremos xml en diccionario para 
    trabajarlo más rapido.
    ---
    \n
    @tStruct : (dict) diccionario a convertir en un diccionario.
    """
    def get_rules_dict(self, tStruct):
        #convertimos a ElementTree
        mido = ElementTree.fromstring(tStruct)
        result = {} #creamos un diccionario para enviarlo.
        for node in mido.iter():
            if node.tag != 'prestashop':
                dicto = node.attrib #tiramos los atributos.
                result[str(node.tag)] = dicto # los colocamos en una llave.
        del result[list(result)[0]] #Eliminamos el primero caracter, para que sea má rapido el control posterior
        return result

    """
    def add_control: funcion para controlar los datos enviados.
    \n
    @data : (dict) contiene los datos que luego se enviaran para guardar
    @data_control : (dict) datos de la estructura para controlar si esta todo correcto.
    """
    def add_control(self, data, data_control):
        print(data)
        msgError = ""   #definimos una variable de recolección de mensajes y otros.
        for reg in data:    #comenzamos a recorrer.
            if reg != "id": #id es un campo que no aparece en el control de datos.
                #Empezamos con el control de Formato,
                #Aqui se puede definir en self.dict_format una funcion para 
                #comprobar cada uno de los tipos. Se puede modificar la funcion
                #pero lo importante es definir como corresponde la funcion a llamar.
                if data_control[reg]['format'] in self.dict_format:
                    if data[reg] != '':
                        self.line_for_format = data[reg] #Este es una variable importante.
                        resultado = self.dict_format[data_control[reg]['format']]()
                        if resultado[0] == False:
                            msgError += resultado[1]
                #comprobamos si es un campo requerido
                if 'required' in data_control[reg]:
                    isRequired = data_control[reg]['required']
                        #if data[reg] == '':
                    #por lo general esta en 'true' por las dudas se deja para hacer una segunda comprobación.
                    if isRequired == 'true' and data[reg] == '':
                            msgError += "El registro {} no tiene valores y son requeridos. \n".format(reg)
                #Ahora comprobamos si el tamaño excede.
                if 'maxSize' in data_control[reg]:
                    maxSize = int(data_control[reg]['maxSize'])
                    if data[reg] != '':
                        if len(data[reg]) > maxSize:
                            msgError += "El registro {} tiene más valores que el maximo permitido: {} y este campo tiene: {}. \n".format(reg, maxSize, len(data[reg]))
        #Si no entraron errores devolvera True, y un campo vacio.
        if msgError == "":
            return True, msgError
        else:
            #Aqui es que se encontraron errores.
            return False, msgError     

    def get_struct(self, resource, schema='blank', type_json=True):
        self.define_json(type_json=type_json)
        self.set_params_get(resource=resource, schema=schema)
        struct = self.executeRequest()
        if type_json == True:
            return struct.json()
        return struct.text
    
    def add_get(self, resource, rec_id=True):
        """
        ```
        def add_get : esto devolvera un diccionario con tres fases,
        1) struct    : la estructura a completar. (JSON)
        2) rules     : las reglas si son requeridas o que. (Esto se realiza aquí porque si se quiere utilizar para antes de hacerlo en segunda instancia.)
        3) relations : esto dependera de rec_id si esta en True, completara las relaciones correspondientes a cada uno. 
        ---
        @resource : (string) recurso con el que vamos a trabajar.
        @rec_id   : (boolean) si se recuperan las relaciones para luego poder utilizarlas.
        ```
        """
        #primero trabajaremos con la estructura.
        struct = self.get_struct(resource=resource)   #traemos los datos.
        struct = struct[list(struct)[0]]                        #traemos la primer key del diccionario
        #print(struct)
        #ahora vamos por las reglas.
        tStruct = self.get_struct(resource=resource, schema='synopsis', type_json=False)                             #recuperamos
        tStruct = self.get_rules_dict(tStruct=tStruct)         #convertimos a xml el diccionario.
        tmp = {}                # Creamos un diccionario que utilizaremos.
        relat_id = {}           
        if rec_id == True:      # si es true traera los datos relativos.
            rel = relations()   # iniciamos los diccionarios de relaciones.
            for field_struct in struct:             #Recurremos la estructura para comprobar cada campo si es de relacion o no.
                if "id_" == field_struct[:3]:       #Si comienza en id_ tenemos un campo relacionado.
                    values = rel.relations[field_struct] #Buscamos los valores. nombre recurso, y valor
                    relat_id[values[0]] = self.g_id_name(resource=values[0],name=values[1])
        #Completamos todos los datos de la estructura.
        tmp['struct'] = struct 
        tmp['rules'] = tStruct
        tmp['relations'] = relat_id
        tmp['resource'] = resource
        return tmp


    def add(self, data, comp_dat=True):
        """
        ```
        def add: función para agregar un registro.
        @resource : (string) nombre del recurso al que deseamos acceder.
        @data : (dict) debe devolverse el diccionario completo.
        @comp_dat : (boolean) Si se comprobaran los datos.  
        ```
        """
        print(data['struct'])
        result = ""                     # variable que tendra el resultado de el intento de carga.
        if comp_dat == True:            #Comenzaremos la compración de datos si es TRUE.
            result = self.add_control(data['struct'], data['rules']) #Llamamos a add_control
            if result[0] == False:                                   # si el Resultado es False cortamos la ejecucion y enviamos el error.
                return result                   #Si hubo error.
        #Comenzamos a trabajar con la parte que importa.
        info = {}
        info[data['resource']] = data['struct'] #comenzamos a dar el formato que necesita el xml.
        result = self.save(data['resource'], info)
        return result


    def save(self, resource, data):
        self.set_params_get(resource)
        self.define_json(False)
        data = dicttoxml.dicttoxml(data, attr_type=False, custom_root='prestashop') #convertimos en xml
        result = self.executeRequest(method='POST',data=data) #llamamos a executeRequest para enviar los datos.         
        return result
    
    #
    #-------------- DELETE -----------------
    #Sector para la eliminación de registro.
    #---------------------------------------

    def clear_headers(self):
        self.default_headers['Content-type'] = ''
        self.default_headers['Io-Format'] = ''
        self.default_headers['Output-Format'] = ''
        
    def delete(self, resource, id):
        """
        ```
        def delete(): Borra una entidad
        resource (str) # cadena que contiene el host adonde debemos acceder.
        id       (str) # cadena con la clave que nos entrego PrestaShop
        return boolean, str
        ```
        """
        self.clear_headers()
        self.set_params_get(resource=resource, id=str(id), schema='')
        result = self.executeRequest(method='DELETE')
        msg = self.checkStatusCode(result.status_code)
        if result.status_code == 200:
            return True, msg

        return False, msg



    
    def fun(self):
        """
        ```
        def fun : Esta funcion simplemente es el esquema para poder personalizar cada
        una de las comprobaciones.
        ```
        """
        # lo que se debe tomar el self.line_for_format para comprobar como 
        #string de comprabacion
        #self.line_for_format
        return True, ''


    