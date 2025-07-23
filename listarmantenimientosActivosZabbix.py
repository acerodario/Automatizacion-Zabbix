import requests
import json
import urllib3
from datetime import datetime

# Deshabilitar advertencias de certificados no seguros
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


url = "https://---------.zabbix/api_jsonrpc.php"


zabbix_token = "TOKEN"

# Crear el payload para la solicitud
payload = json.dumps({
    "jsonrpc": "2.0",
    "method": "maintenance.get",
    "params": {
        "output": ["name", "maintenanceid", "active_since", "active_till", "description"],
        "filter": {
            "status": 0  
        },
        "selectHostGroups": "extend",
        "selectTimeperiods": "extend",
        "selectTags": "extend"
    },
    "auth": zabbix_token,
    "id": 1
})

# Cabeceras de la solicitud
headers = {
    'Content-Type': 'application/json'
}

# Hacer la solicitud POST a la API de Zabbix
try:
    response = requests.post(url, headers=headers, data=payload, verify=False)
    response.raise_for_status()  # Lanza una excepción si la respuesta no es exitosa

    
    data = response.json()

    # Verificar si hay un error en la respuesta
    if "error" in data:
        print(f"Error en la API: {data['error']['data']}")
    else:
        
        for mantenimiento in data.get("result", []):
            name = mantenimiento.get("name")
            maintenanceid = mantenimiento.get("maintenanceid")
            active_since = mantenimiento.get("active_since")
            active_till = mantenimiento.get("active_till")
            description = mantenimiento.get("description", "Sin descripción disponible")

          
            readable_start = datetime.fromtimestamp(int(active_since))
            readable_end = datetime.fromtimestamp(int(active_till))

       
            print(f"Mantenimiento: {name}")
            print(f"ID: {maintenanceid}")
            print(f"Descripción: {description}")
            print(f"Activo desde: {readable_start.strftime('%d/%m/%Y, %I:%M:%S %p')}")
            print(f"Activo hasta: {readable_end.strftime('%d/%m/%Y, %I:%M:%S %p')}")
            print("-" * 50)

except requests.exceptions.RequestException as e:
    print(f"Error en la solicitud: {e}")
