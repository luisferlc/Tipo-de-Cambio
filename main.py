import json
from sie_banxico import SIEBanxico


## Open token file
with open("token.json") as infile:
    json_obj = json.load(infile)
    token = json_obj["token"]

# Series: 
"""
SF43718 - Pesos por Dólar. FIX: Esta serie representa el tipo de cambio FIX. 
El tipo de cambio FIX es determinado por el Banco de México y publicado en el Diario Oficial de la Federación. 
Se utiliza en operaciones denominadas en dólares pagaderas en la República Mexicana1
"""
id_series = ["SF43718"]

# Crea una instancia de la API
api = SIEBanxico(token=token, id_series=id_series, language='es')

# Ahora puedes hacer consultas a la API
#metadata = api.get_metadata()
last_data = api.get_lastdata()

# Accede a los datos utilizando las claves
serie = last_data['bmx']['series'][0]
id_serie = serie['idSerie']
titulo = serie['titulo']
fecha = serie['datos'][0]['fecha']
dato = serie['datos'][0]['dato']

print(f"idSerie: {id_serie}")
print(f"titulo: {titulo}")
print(f"fecha: {fecha}")
print(f"dato: {dato}")



