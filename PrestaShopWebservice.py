#Imports generales
import requests
import os.path
import json
import dicttoxml

from xml.etree import ElementTree

#Imports particulares
from const_rel import relations

class PrestaShopWebservice:
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
        self.other_params = {
                            'filter' : '',
                            'sort' : '',
                            'limit' : '',
                            'id_shop' : '',
                            'id_group_shop' : ''
                            }
        self.psCompatibleVersionsMin = '1.7.0.0'            #La minima versión comprobada que funciona con esta APP
        self.psCompatibleVersionsMax = '1.7.99.99'          #La maxima versión comprobada que funciona con esta APP
        self.protocol = protocol + "://"                    #creamos la cadena para el protocolo
        self.dir_cache = "cache/"                           #configuracion de la carpeta que hara de cache
        self.define_json()                                  #le asignamos valores por defecto a la cabecera sobre entrada y salida de datos.

    """
    def checkStatusCode: Control del estado de las peticiones.
    ---\n
    @status_code: (int) Numero de respuesta de la peticion realizada.\n
    """
    def checkStatusCode(self, status_code):
        error_label = 'ERROR!... \n This call to PrestaShop Web Services failed and returned an HTTP status of {}. \n That means: {}. \n Details: {}.'
        msg_label = 'OK!... \n This call to Prestashop Web Services returned an HTTO status of {}. \n That means: {}. \n Details: {}.'
        case = {200 : error_label.format(status_code, 'Ok', 'Respuesta estándar para peticiones correctas.'),
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
                               headers=self.default_headers,
                               data=data,
                               auth=(self.key,'')
                               )
        response = session.send(req.prepare(), verify=True)
        return response

    """
    def set_params_get: para setear los parametros.
    \n
    @resource : (str)
    @id : (str)
    @schema : (str)
    """
    def set_params_get(self, resource=False, id=False, schema=False):
        #Todos los args son opcionales, si no se coloca nada borrara los valores.j
        #en caso de que se envien valores se modificaran.
        self.default_params['resource'] = resource if resource != False else ''
        self.default_params['id'] = id if id != False else ''
        self.default_params['schema'] = schema if schema != False else ''

    """
    def make_param:
    \n
    """
    def make_param(self):
        other_params = ""
        for k, v in self.other_params.items():
            if v != "":
                other_params += k+"="+v+"&"
        other_params = other_params.strip()
        return other_params[:-1]

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
        new_param = self.make_param()
        if "?" in url:
            url = url + "&" + new_param if new_param != '' else url
        else:
            url = url + "?" + new_param if new_param != '' else url 
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
            #self.default_headers['Content-Type'] = 'application/json'
        else:
            self.default_headers['Output-Format'] = 'XML'
            self.default_headers['Io-Format'] = 'XML'
            self.default_headers['Content-Type'] = 'text/xml'



    #
    #-------------- ADD ----------------
    #Sector para el agregado de valores.
    #-----------------------------------


    def get_id_name(self, resource, name):
        update = True
        self.define_json() #definimos el tipo de pedido que vamos a realizar
        self.set_params_get(resource=resource)
        rec = self.executeRequest()
        if len(rec.json()) > 0:
            rec = rec.json()[resource]
        else:
            update = False
        if update == True:
            path = self.dir_cache + resource + ".json"
            if os.path.isfile(path):
                cmp_json = json.load(open(path, "r"))
                if cmp_json == rec:
                    update = False
                else:
                    file_object = open(path, "w")
                    json.dump(rec, file_object)
            else:
                file_object = open(path, "w")
                json.dump(rec, file_object)
            path_detail = self.dir_cache + resource + "Detail" + ".json"
            if update:
                id_name = {}
                for ix in rec:
                    self.set_params_get(resource=resource, id=str(ix['id']))
                    new_rec = self.executeRequest().json()
                    if "," in name:
                        fullName = ""
                        arrayName = name.split(",")
                        for tmpName in arrayName:
                            fullName += new_rec[str(list(new_rec)[0])][tmpName] + " "
                        id_name[str(ix['id'])] = fullName[:-1]    
                    else:    
                        id_name[str(ix['id'])] = new_rec[str(list(new_rec)[0])][name]
                file_object = open(path_detail, "w")
                json.dump(id_name, file_object)
            else:
                id_name = json.load(open(path_detail, "r"))
        else:
            id_name = {'1' : 'No data found'}
        return id_name

    
    def get_rules_dict(self, tStruct):
        mido = ElementTree.fromstring(tStruct)
        result = {}
        for node in mido.iter():
            if node.tag != 'prestashop':
                dicto = node.attrib
                result[str(node.tag)] = dicto
        del result[list(result)[0]]
        return result



    def get_add(self, resource, rec_id=True):
        self.define_json()
        self.set_params_get(resource=resource, schema='blank')
        struct = self.executeRequest().json()
        struct = struct[list(struct)[0]]
        self.define_json(type_json=False)
        self.set_params_get(resource=resource, schema='synopsis')
        tStruct = self.executeRequest()
        tStruct = self.get_rules_dict(tStruct=tStruct.text)
        tmp = {}
        relat_id = {}
        if rec_id == True:    
            rel = relations()
            for field_struct in struct:
                if "id_" == field_struct[:3]:
                    values = rel.relations[field_struct]
                    relat_id[values[0]] = self.get_id_name(resource=values[0],name=values[1])
        tmp['struct'] = struct
        tmp['rules'] = tStruct
        tmp['relations'] = relat_id
        return tmp

    def add(self, resource, data, comp_dat=True):
        self.define_json(False)
        self.set_params_get(resource)
        info = {}
        info[resource] = data['struct']
        data = dicttoxml.dicttoxml(info, attr_type=False, custom_root='prestashop')
        result = self.executeRequest(method='POST',data=data)
        return result

