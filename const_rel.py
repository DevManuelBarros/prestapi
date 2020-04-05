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
            'id_address' : ['addresses' , 'id,alias'],
            'id_zone' : ['zones', 'id,name'],
            'id_default_group' : ['groups','id,name'],
            'id_lang' : ['languages', 'id,name'],
            'id_gender' : ['Gender','None'],
            'id_risk'   : ['Risk', 'None'],
            'id_shop'   : ['shops', 'id,name'],
            'id_shop_group' : ['shop_groups', 'id,name'],
            'id_category_default' : ['categories', 'id,name'],
            'id_default_images' : ['images', 'id,name'],
            'id_default_combination' : ['combinations', 'id,name'],
            'id_tax_rules_group' : ['tax_rule_group', 'id,name']
             
        }

