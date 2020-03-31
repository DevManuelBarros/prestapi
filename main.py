from PrestaShopWebservice import PrestaShopWebservice


obj = PrestaShopWebservice(host="cristalgrafargentina.com/", protocol="https", key="4KUR3FXBD5TD9ZJJGXDW9W6B6P1TR72I")
#obj.set_params_get(resource="warehouses", schema='blank')
#tmp = obj.executeRequest()


#tmp = obj.get_add(resource="addresses")
"""
tmp['alias']  = 'My address'
tmp['lastname'] = 'DOE'
tmp['firstname'] = 'JHON'
tmp['address1'] = 'Una direccion'
tmp['postcode'] = '75009'
tmp['city'] = 'Paris'
tmp['id_country'] = 1 
"""
tmp = obj.get_id_name('id_country')
#print(tmp)
