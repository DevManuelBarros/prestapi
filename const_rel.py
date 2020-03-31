class relations:

    def __init__(self):
        #Lo que tenga
        self.relations = {
            'id_country' : ['countries', 'name'],
            'id_supplier' : ['suppliers', 'name'], 
            'id_customer' : ['customers','lastname,firstname'],  
            'id_manufacturer' : ['manufacturers', 'name'],
            'id_warehouse' : ['warehouses', 'name'],
            'id_state' : ['states', 'name'],
            'id_address' : ['addresses' , 'alias']
        }

