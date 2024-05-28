
import json
import datetime
from sie_banxico import SIEBanxico
import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

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

dag = DAG(
    dag_id="tipo_cambio_mx_us",
    start_date=datetime(2024,5,28),
    schedule_interval="@daily"
)

def _get_banxico_data():
    ## Open token file
    with open("token.json") as infile:
        json_obj = json.load(infile)
        token = json_obj["token"]

    # Series: 
    id_series = ["SF43718"]

    # Crea una instancia de la API
    api = SIEBanxico(token=token, id_series=id_series, language='es')

    # Ahora puedes hacer consultas a la API
    last_data = api.get_lastdata()


get_tipo_cambio = PythonOperator(
    task_id="get_tipo_cambio",
    python_callable= _get_banxico_data,
    dag=dag,
)

def print_tipo_cambio_results():
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

notify = BashOperator(
    task_id="notify",
    bash_command= print_tipo_cambio_results,
    dag=dag
)






