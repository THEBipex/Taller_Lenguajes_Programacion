import  requests
from datetime import datetime

FERIADOS_API = "https://api.boostr.cl/holidays.json"

def obtener_tipo_feriado(fecha: datetime.date):
    """
    Retorna el tipo de feriado para una fecha dada:
    - 'irrenunciable'
    - 'normal'
    - 'no'
    """
    try: 
        response = requests.get(FERIADOS_API, timeout=5)
        feriados = response.json()

        fecha_str = fecha.strftime('%Y-%m-%d')
        for feriado in feriados:
            if feriado['fecha'] == fecha_str:
                if feriado.get('irrenunciable', False):
                    return 'irrenunciable'
                return 'normal'
        return 'no'
    except Exception as e:
        print("Error al consultar feriados: ", e)
        return 'no'
        