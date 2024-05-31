
import json
import pendulum
from sie_banxico import SIEBanxico
import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# Create a timezone object for UTC-6
timezone = pendulum.timezone('Etc/GMT+6')

dag = DAG(
    dag_id="tipo_cambio_mx_us",
    start_date=pendulum.datetime(2024,5,28, 11, 0, tz = timezone),
    schedule_interval='0 11 * * *'
)

def _get_banxico_data():
    ## Open token file
    with open("/opt/airflow/files/token.json") as infile: #carpeta creada en la carpeta docker airflow.
        json_obj = json.load(infile)
        token = json_obj["token"]

    # Series: 
    id_series = ["SF43718"]

    # Crea una instancia de la API
    api = SIEBanxico(token=token, id_series=id_series, language='es')

    # Ahora puedes hacer consultas a la API
    last_data = api.get_lastdata()
    
    return last_data


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

notify = PythonOperator(
    task_id="notify",
    python_callable= print_tipo_cambio_results,
    dag=dag
)