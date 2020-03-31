class relations:

    def __init__(self):
        #Lo que tenga
        self.relations = {
            'id_country' : ['countries'],
            'id_supplier' : ['suppliers'], 
            'id_customer' : ['customers','lastaname,firstname'],  
            'id_manufacturer' : ['manufacturers'],
            'id_warehouse' : ['warehouses'],
            'id_state' : ['states'],
        }

