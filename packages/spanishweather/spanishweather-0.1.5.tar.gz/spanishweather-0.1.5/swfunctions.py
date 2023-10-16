import json
import requests
import urls

def GetDatosJson(self, url):
        headers = {'accept' : 'application/json'}         
        response = requests.request("GET",url, headers = headers, params = urls.api_key)
        response = response.json()
        url_datos = response['datos']
        response_datos = requests.get(url_datos)
        response_datos = response_datos.text
        datos = json.loads(response_datos)
        datos = json.dumps(datos, indent=4)                
        