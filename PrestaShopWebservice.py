import requests
import os.path
import json
from xml.etree import ElementTree
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
        #string Shop url
        self.host = host
        #string Authentification key
        self.key = key
        #boolean is debug activated
        self.debug = debug
        #string PS version
        self.version = 'unknown'
        #default settings headers
        self.default_headers = {
                                'Io-Format' : '',
                                'Output-Format' : '',
                                'User-Agent': 'PrestaShopWebservice.py by Manuel Barros',
                              }
        #default settings params
        self.default_params = {'resource':'',
                                'id':'',
                                'schema' : ''}
        self.other_params = {
                            'filter' : '',
                            'sort' : '',
                            'limit' : '',
                            'id_shop' : '',
                            'id_group_shop' : ''
                            }
        #Min. Version compatible with this module
        self.psCompatibleVersionsMin = '1.7.0.0'
        #Max. Version compatible with this module
        self.psCompatibleVersionsMax = '1.7.99.99'
        self.protocol = protocol + "://"
        self.dir_cache = "cache/"
        self.define_json()

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
        if add == True:
            for k, v in params.items():
                self.default_params[k] = v
        else:
            self.default_params = params
        return self.default_params
    """
    def change_headers: Agrega o cambia totalmente los parametros
    ---\n
    @params : (dict) Los parametros a agregar o colocar dentro del diccionario por default\n
    @add : (bool) si estan en True, como por defecto, agrega al diccionario o en caso contrario modifica totalmente la cabecera\n
    """
    def change_headers(self, headers={}, add=True):
        if add == True:
            for k, v in headers.items():
                self.default_headers[k] = v
        else:
            self.default_headers = headers
        return self.default_headers
    
    """
    def executeRequest: Metodo interno para terminar de ejecutar la peticion con requests
    ---\n
    """
    def executeRequest(self,  method='GET', url=False):
        if url == False:
            url_full = self.make_full_url()
        else:
            url_full = url
        session = requests.Session()
        req = requests.Request(method, 
                               url_full,
                               headers=self.default_headers,
                               auth=(self.key,'')
                               )
        response = session.send(req.prepare(), verify=True)
        return response


    def set_params_get(self, resource=False, id=False, schema=False):
        self.default_params['resource'] = resource if resource != False else ''
        self.default_params['id'] = id if id != False else ''
        self.default_params['schema'] = schema if schema != False else ''


    def make_param(self):
        other_params = ""
        for k, v in self.other_params.items():
            if v != "":
                other_params += k+"="+v+"&"
        other_params = other_params.strip()
        return other_params[:-1]


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

    def define_json(self, type_json=True):
        if type_json==True:
            self.default_headers['Output-Format'] = 'JSON'
            self.default_headers['Io-Format'] = 'JSON'
        else:
            self.default_headers['Output-Format'] = 'XML'
            self.default_headers['Io-Format'] = 'XML'

    def get_id_name(self, rel_field):
        tmpRel = relations() #obtenemos el diccionario con los datos para recuperar
        new_resource = tmpRel.relations[rel_field]
        self.define_json() #definimos el tipo de pedido que vamos a realizar
        self.set_params_get(resource=new_resource[0])
        rec = self.executeRequest().json()[new_resource[0]]
        path = self.dir_cache + new_resource[0]+ ".json"
        if os.path.isfile(path):
            cmp_json = json.load(open(path, "r"))
            if cmp_json == rec:
                print("Es igual")
            else:
                print("No es igual")
        else:
            file_object = open(path, "w")
            json.dump(rec, file_object)

        """
        for ix in rec:
            self.set_params_get(resource=new_resource[0],id=str(ix['id']))
            new_rec = self.executeRequest().json()  
            print(new_rec[str(list(new_rec)[0])]['name'])
        """
    
    
    def get_rules_dict(self, resource, tStruct):
        mido = ElementTree.fromstring(tStruct)
        result = {}
        for node in mido.iter():
            if node.tag != 'prestashop' and node.tag != resource:
                dicto = node.attrib
                result[str(node.tag)] = dicto
        return result

    def get_add(self, resource, rec_id=True):
        self.define_json()
        self.set_params_get(resource=resource, schema='blank')
        struct = self.executeRequest()
        struct = struct.json()
        struct = struct[list(struct.keys())[0]]
        self.define_json(type_json=False)
        self.set_params_get(resource=resource, schema='synopsis')
        tStruct = self.executeRequest()
        tStruct = self.get_rules_dict(resource=resource, tStruct=tStruct.text)
        tmp = {}
        if rec_id == True:
            rel = relations()
        tmp['struct'] = struct
        tmp['rules'] = tStruct
        return tmp

    def add(self, resource, json):
        pass

