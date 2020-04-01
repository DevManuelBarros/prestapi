class relations:

    def __init__(self):
        #Lo que tenga
        self.relations = {
            'id_country' : ['countries', 'id,name'],
            'id_supplier' : ['suppliers', 'id,name'], 
            'id_customer' : ['customers','id,lastname,firstname'],  
            'id_manufacturer' : ['manufacturers', 'id,name'],
            'id_warehouse' : ['warehouses', 'id,name'],
            'id_state' : ['states', 'id,name'],
            'id_address' : ['addresses' , 'id,alias']
        }

