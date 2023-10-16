import urls

class SpecificPredictions:
    
    def __init__(self):
        pass
    
    def GetMontanyaPasada(self, AreaMontanyosa): 
        
        # Breve resumen con lo más significativo de las condiciones meteorológicas registradas en la zona de montaña que se pasa como parámetro (area) en las últimas 24-36 horas. 
                    
        url = urls.url_base + urls.urls[0][1] + AreaMontanyosa + "/" 
        datos = self.GetDatosJson(url)                    
        return datos
    
    def GetNieveArea(self, Area):
        
        # Información nivológica para la zona montañosa que se pasa como parámetro (area).
        
        if Area not in ['0','1']:
            raise ValueError("El parametro area solo puede ser 0 o 1")
                
        try:         
            url = urls.url_base + urls.urls[2][1] + Area + "/" 
            datos = self.GetDatosJson(url) 
            return datos
        except ValueError as e:
            print("Error ", e)
    
    def GetMontanyaDia(self, AreaMontanyosa, Dia):
        
        # Predicción meteorológica para la zona montañosa que se pasa como parámetro (area) con validez para el día (día). Periodicidad de actualización: continuamente. 
        
        # 0	día actual 1d+1 (mañana) 
        # 1	d+1 (mañana)
        # 2	d+2 (pasado mañana)     
        # 3	d+3 (siguente a pasado mañana) 
        
        if Dia not in ['0','1','2','3']:
            raise ValueError("El parametro dia debe ser mayor o igual a 0 y menor o igual 3")
                
        try:         
            url = urls.url_base + urls.urls[0][1] + AreaMontanyosa + "/dia/" + Dia + "/" 
            datos = self.GetDatosJson(url) 
            return datos
        except ValueError as e:
            print("Error ", e)
      
    def GetMunicipioDiaria(self, CodigoMunicipio):  
        
        # Predicción para el municipio que se pasa como parámetro (municipio). Periodicidad de actualización: continuamente. 
        
        url = urls.url_base + urls.urls[2][1] + CodigoMunicipio + "/" 
        datos = self.GetDatosJson(url)                    
        return datos      
    
    def GetMunicipioHoraria(self, CodigoMunicipio):
        
        # Predicción horaria para el municipio que se pasa como parámetro. Presenta la información de hora en hora hasta 48 horas.
        
        url = urls.url_base + urls.urls[3][1] + CodigoMunicipio + "/" 
        datos = self.GetDatosJson(url)                    
        return datos
    
    def GetPlaya(self, CodigoPlaya):
        
        # La predicción diaria de la playa que se pasa como parámetro. Establece el estado de nubosidad para unas horas determinadas, las 11 y las 17 hora oficial. Se analiza también si se espera precipitación en el entorno de esas horas, entre las 08 y las 14 horas y entre las 14 y 20 horas.
        
        url = urls.url_base + urls.urls[4][1] + CodigoPlaya + "/" 
        datos = self.GetDatosJson(url)                    
        return datos
    
    def GetUltravioleta(self, Dia):
        
        # Predicción de Índice de radiación UV máximo en condiciones de cielo despejado para el día seleccionado.
        
        # 0	día actual 
        # 1	d+1 (mañana)
        # 2	d+2 (pasado mañana)     
        # 3	d+3 (dentro de 3 dias)
        # 4	d+4 (dentro de 4 dias)
        
        if Dia not in ['0','1','2','3','4']:
            raise ValueError("El parametro dia debe ser mayor o igual a 0 y menor o igual 3")
                
        try:         
            url = urls.url_base + urls.urls[5][1] + Dia + "/"   
            datos = self.GetDatosJson(url) 
            return datos
        except ValueError as e:
            print("Error ", e)
   
    
   
     