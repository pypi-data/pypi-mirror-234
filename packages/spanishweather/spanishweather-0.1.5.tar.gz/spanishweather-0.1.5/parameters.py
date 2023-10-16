import pandas
import requests
from io import StringIO

class Parametros:

    # Códigos Areas Montañosas

    AreasMontanyosas = {
        'peu1' : 'Picos de Europa',   
        'nav1' : 'Pirineo Navarro',
        'arn1' : 'Pirineo Aragonés',
        'cat1' : 'Pirineo Catalán',
        'rio1' : 'Ibérica Riojana',
        'arn2' : 'Ibérica Aragonesa',
        'mad2' : 'Sierras de Guadarrama y Somosierra',
        'gre1' : 'Sierra de Gredos',
        'nev1' : 'Sierra Nevada'
    }
    
    # Codigos Areas nivologicas
    
    AreasNivologicas = {
        0 : 'Pirineo Catalán',
        1 : 'Pirineo Navarro y Aragonés'
    }    
   
    # Codigos Municipios

    url = 'https://www.ine.es/daco/daco42/codmun/codmun20/20codmun.xlsx'
    df_municipios = pandas.read_excel(url, header = 1)
    df_municipios = df_municipios.astype(str)
    nombrescolumna = ["CodigoAutonomia","CodigoProvincia","CodigoMunicipio","DC","NombreMunicipio"]
    df_municipios.columns = nombrescolumna
    df_municipios['CodigoProvincia'] = df_municipios['CodigoProvincia'].apply(lambda x: x.zfill(2))
    df_municipios['CodigoMunicipio'] =  df_municipios['CodigoMunicipio'].apply(lambda x: x.zfill(3))
    df_municipios['idMunicipio'] = df_municipios['CodigoProvincia'] + df_municipios['CodigoMunicipio']
    
    # Codigos Playas
    
    url = 'https://www.aemet.es/documentos/es/eltiempo/prediccion/playas/Playas_codigos.csv'    
    response = requests.get(url)
    csv_content = response.text
    csv_io = StringIO(csv_content)
    df_playas = pandas.read_csv(csv_io, delimiter=';')
    nombrescolumna = ["idPlaya","NombrePlaya","idProvincia","NombreProvincia","idMunicipio","NombreMunicipio","Latitud","Longitud"]
    df_playas.columns = nombrescolumna
    
   
    def __init__(self):
        pass

    def __del__(self):
        pass

    def GetCodigoAreaMontanya(self, nombre):
        nombre
        
    def GetidMunicipio(self, nombre):
        col = Parametros.df_municipios['NombreMunicipio']
        cod = Parametros.df_municipios.loc[col.str.contains(nombre, case=False, na=False)]
        return cod
    
    def GetCodigoPlaya(self, nombre):
        col = Parametros.df_playas['NombrePlaya']
        cod = Parametros.df_playas.loc[col.str.contains(nombre, case=False, na=False)]
        dic = dict(zip(cod['idPlaya'],cod['NombrePlaya']))       
        return dic