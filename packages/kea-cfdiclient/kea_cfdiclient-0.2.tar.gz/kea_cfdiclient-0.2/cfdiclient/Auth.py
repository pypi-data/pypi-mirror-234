import requests
from datetime import datetime
# -*- coding: utf-8 -*-
from cfdiclient.Fiel import Fiel
from dateutil.relativedelta import relativedelta
from cfdiclient.utils import Utils
from cfdiclient.format_strings import FormatStrings

class AuthFiel:
    def __init__(self, fiel: Fiel):
        self.fiel = fiel
        self.utils = Utils()
        self.format_strings = FormatStrings()

    soap_action = 'http://DescargaMasivaTerceros.gob.mx/IAutenticacion/Autentica'
    url = 'https://cfdidescargamasivasolicitud.clouda.sat.gob.mx/Autenticacion/Autenticacion.svc'
    
    def soapRequest(self, token_lifetime=5, token_lifetime_unit='minutes'):
        xml = self.getSOAPBody(token_lifetime, token_lifetime_unit)
        headers = self.utils.headers(xml=xml, soapAction=self.soap_action)
        
        soap_request = requests.post(url=self.url, data=xml, headers=headers, timeout=10)

        xmlResponse = soap_request.text
        tree = self.utils.xml_etree(xmlResponse)
        
        # Encontrar el elemento AutenticaResult
        AutenticaResultElement = tree.find(".//{http://DescargaMasivaTerceros.gob.mx}AutenticaResult")
        
        if AutenticaResultElement is not None:
            sat_token = AutenticaResultElement.text
            return sat_token
        else:
            print(AutenticaResultElement)
            raise Exception("No se pudo obtener el token del SAT, intenta más tarde")
            #Raise error
        
        
    def getSOAPBody(self, token_lifetime=5, token_lifetime_unit='minutes'):
        
        uuid = self.utils.generateUUID()
        
        fecha_inicial = datetime.today().utcnow()
        
        if token_lifetime_unit == 'minutes':
            fecha_final =  fecha_inicial + relativedelta(minutes=token_lifetime)
        
        if token_lifetime_unit == 'hours':
            fecha_final =  fecha_inicial + relativedelta(hours=token_lifetime)
        
        if token_lifetime_unit == 'days':
            fecha_final =  fecha_inicial + relativedelta(days=token_lifetime)
        
        if token_lifetime_unit == 'weeks':
            fecha_final =  fecha_inicial + relativedelta(weeks=token_lifetime)
        
        if token_lifetime_unit == 'months':
            fecha_final =  fecha_inicial + relativedelta(months=token_lifetime)
        
        if token_lifetime_unit == 'years':
            fecha_final =  fecha_inicial + relativedelta(years=token_lifetime)
        
        fecha_inicial = fecha_inicial.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        fecha_final = fecha_final.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        
        data = self.format_strings.format_date(fecha_inicial, fecha_final)
        
        digest_value = self.utils.b64_sha1_digest(data)

        dataToSign = self.format_strings.signature_value(digest_value)
        
        signature_value = self.fiel.firmar_sha1(bytes(dataToSign, 'UTF-8')).decode('UTF-8')

        #BinarySecurityToken
        b64certificate = self.fiel.cer_to_base64().decode("utf-8")

        xml = self.format_strings.xml_authentication(fecha_inicial, fecha_final, uuid, b64certificate, digest_value, signature_value)

        xml = xml.encode('utf-8')

        return xml